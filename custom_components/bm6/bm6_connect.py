"""This module implements communication with BM6 device."""

from __future__ import annotations

import asyncio
from contextlib import suppress
from dataclasses import dataclass
import logging
from enum import Enum
from time import monotonic
from typing import Optional

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.scanner import AdvertisementData
from bleak_retry_connector import establish_connection
from Crypto.Cipher import AES

from habluetooth import BaseHaScanner, BluetoothScannerDevice
from homeassistant.core import HomeAssistant
from homeassistant.components.bluetooth import async_scanner_devices_by_address

from .const import (
    CHARACTERISTIC_UUID_NOTIFY,
    CHARACTERISTIC_UUID_WRITE,
    CRYPT_KEY,
    BLEAK_CLIENT_TIMEOUT,
    GATT_DATA_REALTIME,
    GATT_DATA_VERSION,
    GATT_NOTIFY_REALTIME_PREFIX,
    GATT_NOTIFY_VERSION_PREFIX,
)

_LOGGER = logging.getLogger(__name__)


class BM6RealTimeState(Enum):
    """Enumeration for BM6 device status."""

    BatteryOk = 0
    LowVoltage = 1
    Charging = 2


@dataclass
class BM6RealTimeData:
    """Class to store the real-time data read from the BM6 device."""

    Voltage: float = 0.0  # Battery voltage in V
    Temperature: int = 0  # Temperature in °C
    Percent: int = 0  # Percentage of power in %
    RapidAcceleration: int = 0
    RapidDeceleration: int = 0
    State: BM6RealTimeState = BM6RealTimeState.BatteryOk  # Status of the battery

    def __init__(self, data: str):
        """Initialize BM6ReadTimeData from a hex string."""
        self.Voltage = int(data[14:18], 16) / 100
        temperature_sign = int(data[6:8], 16)
        self.Temperature = int(data[8:10], 16)
        if temperature_sign == 1:
            self.Temperature = -self.Temperature
        self.Percent = int(data[12:14], 16)
        self.RapidAcceleration = int(data[18:22], 16)
        self.RapidDeceleration = int(data[22:26], 16)
        self.State = int(data[10:12], 16)


@dataclass
class BM6Firmware:
    """Class to store the firmware version of the BM6 device."""

    Version: str = None

    def __init__(self, data: str):
        """Initialize BM6Firmware with version data."""
        self.Version = data


@dataclass
class BM6Advertisement:
    """Class to store the advertisement data of the BM6 device."""

    RSSI: int = None
    Scanner: str = None

    def __init__(
        self,
        advertisement_data: Optional[AdvertisementData],
        ha_scanner: Optional[BaseHaScanner],
    ):
        """Initialize BM6Advertisement with advertisement data."""
        self.RSSI = advertisement_data.rssi if advertisement_data else None
        self.Scanner = ha_scanner.name if ha_scanner else None


@dataclass
class BM6Data:
    """Class to store all data read from the BM6 device."""

    Firmware: Optional[BM6Firmware] = None
    RealTime: Optional[BM6RealTimeData] = None
    Advertisement: Optional[BM6Advertisement] = None

    def __init__(
        self,
        advertisement_data: Optional[AdvertisementData],
        ha_scanner: Optional[BaseHaScanner],
    ):
        """Initialize BM6Data with advertisement data."""
        self.Advertisement = BM6Advertisement(advertisement_data, ha_scanner)


class BM6DeviceError(RuntimeError): ...


class BM6Connector:
    """Class to manage the connection to the BM6 device."""

    def __init__(
        self,
        hass: HomeAssistant,
        address: str,
    ):
        """Initialize the BM6Connector with either a HASS or a BLEDevice."""
        self.hass = hass
        self._address: str = address
        self._scanners: list[BluetoothScannerDevice] = None
        self._data: BM6Data = None
        _LOGGER.debug("Get device BM6 at %s from HASS", self._address)
        self._scanners: list[BluetoothScannerDevice] = async_scanner_devices_by_address(
            hass,
            self._address,
            connectable=True,
        )
        if not self._scanners:
            raise BM6DeviceError(f"Bluetooth device {self._address} not found")
        self._scanners.sort(key=lambda scanner: scanner.advertisement.rssi, reverse=True)
        _LOGGER.debug(
            "Device BM6 at %s is seen by %d scanner(s): %s",
            self._address,
            len(self._scanners),
            [
                {
                    "scanner": scanner.scanner.name,
                    "rssi": scanner.advertisement.rssi,
                }
                for scanner in self._scanners
            ],
        )

    def _decrypt(self, data: bytearray) -> bytearray:
        """Decrypt the received data using AES."""
        cipher = AES.new(CRYPT_KEY, AES.MODE_CBC, 16 * b"\0")
        return cipher.decrypt(data)

    def _encrypt(self, data: bytearray) -> bytearray:
        """Encrypt the data to be sent using AES."""
        cipher = AES.new(CRYPT_KEY, AES.MODE_CBC, 16 * b"\0")
        return cipher.encrypt(data)

    async def _notify_callback(
        self,
        sender: BleakGATTCharacteristic,
        data: bytearray,
    ):
        """Callback function to handle notifications from the BM6 device."""
        message = self._decrypt(data).hex()
        _LOGGER.debug("Received data from BM6 at %s: %s", self._address, message)
        if message.startswith(GATT_NOTIFY_REALTIME_PREFIX):
            self._data.RealTime = BM6RealTimeData(message)
            _LOGGER.debug(
                "Decoded real-time data from BM6 at %s: %s",
                self._address,
                self._data.RealTime,
            )
        elif message.startswith(GATT_NOTIFY_VERSION_PREFIX):
            self._data.Firmware = BM6Firmware(message)
            _LOGGER.debug(
                "Decoded firmware version from BM6 at %s: %s",
                self._address,
                self._data.Firmware,
            )

    async def _connect_client(self, scanner: BluetoothScannerDevice) -> BleakClient:
        """Create a BLE connection via bleak_retry_connector."""
        scanner_name = scanner.scanner.name
        connect_started = monotonic()
        client = await establish_connection(
            BleakClient,
            scanner.ble_device,
            self._address,
            timeout=BLEAK_CLIENT_TIMEOUT,
        )
        _LOGGER.debug(
            "Connected to BM6 at %s via scanner %s in %.3fs",
            self._address,
            scanner_name,
            monotonic() - connect_started,
        )
        return client

    async def get_data(self) -> BM6Data:
        """Retrieve data from the BM6 device."""
        exceptions: list[Exception] = []
        scanner_count = len(self._scanners)
        for idx, scanner in enumerate(self._scanners, start=1):
            scanner_name = scanner.scanner.name
            scanner_rssi = scanner.advertisement.rssi
            attempt_started = monotonic()
            _LOGGER.debug(
                "Start BM6 read attempt %d/%d at %s via scanner %s (rssi=%s)",
                idx,
                scanner_count,
                self._address,
                scanner_name,
                scanner_rssi,
            )
            client: BleakClient | None = None
            try:
                self._data = BM6Data(scanner.advertisement, scanner.scanner)
                client = await self._connect_client(scanner)

                _LOGGER.debug(
                    "Write to BM6 at %s characteristic %s",
                    self._address,
                    CHARACTERISTIC_UUID_WRITE,
                )
                write_started = monotonic()
                await client.write_gatt_char(
                    CHARACTERISTIC_UUID_WRITE,
                    self._encrypt(bytearray.fromhex(GATT_DATA_REALTIME)),
                    response=True,
                )
                _LOGGER.debug(
                    "Wrote BM6 realtime request at %s in %.3fs",
                    self._address,
                    monotonic() - write_started,
                )

                self._data.RealTime = None
                notify_started = monotonic()
                await client.start_notify(CHARACTERISTIC_UUID_NOTIFY, self._notify_callback)
                _LOGGER.debug(
                    "Started BM6 notify subscription at %s in %.3fs",
                    self._address,
                    monotonic() - notify_started,
                )

                wait_started = monotonic()
                while self._data is None or self._data.RealTime is None:
                    wait_elapsed = monotonic() - wait_started
                    if wait_elapsed >= BLEAK_CLIENT_TIMEOUT:
                        raise TimeoutError(
                            f"Timed out waiting for BM6 real-time payload after {wait_elapsed:.1f}s"
                        )
                    await asyncio.sleep(0.1)

                _LOGGER.debug(
                    "Finished BM6 read attempt %d/%d at %s via scanner %s in %.3fs",
                    idx,
                    scanner_count,
                    self._address,
                    scanner_name,
                    monotonic() - attempt_started,
                )
                return self._data

                # The following code is commented out but can be used to get firmware version data
                # _LOGGER.debug("Write to BM6 at %s characteristic %s", device.address, CHARACTERISTIC_UUID_WRITE)
                # await client.write_gatt_char(CHARACTERISTIC_UUID_WRITE,
                #                              self._encrypt(bytearray.fromhex(GATT_DATA_VERSION)),
                #                              response=True)
                # _LOGGER.debug("Wait for data from BM6 at %s", device.address)
                # self._data.Firmware = None
                # await client.start_notify(CHARACTERISTIC_UUID_NOTIFY,
                #                           self._notify_callback)
                # while self._data is None or self._data.Firmware is None:
                #     await asyncio.sleep(0.5)
                # _LOGGER.debug("Finishing wait for data from BM6 at %s", device.address)
                # await client.stop_notify(CHARACTERISTIC_UUID_NOTIFY)
            except Exception as err:
                err.add_note(f"Using scanner {scanner_name}")
                exceptions.append(err)
                _LOGGER.debug(
                    "BM6 read attempt %d/%d failed at %s via scanner %s",
                    idx,
                    scanner_count,
                    self._address,
                    scanner_name,
                    exc_info=True,
                )
                _LOGGER.warning(
                    "Error while reading BM6 at %s via scanner %s: %s",
                    self._address,
                    scanner_name,
                    err,
                )
            finally:
                if client is not None:
                    with suppress(Exception):
                        await client.stop_notify(CHARACTERISTIC_UUID_NOTIFY)
                    with suppress(Exception):
                        await client.disconnect()

        if exceptions:
            raise BM6DeviceError(
                f"Error while reading BM6 at {self._address}: {exceptions}"
            ) from exceptions[0]

        raise BM6DeviceError(f"Error while reading BM6 at {self._address}")
