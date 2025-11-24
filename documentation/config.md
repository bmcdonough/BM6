# Configuration Directory

This document describes the `config/` directory, which contains Home Assistant configuration files for development and testing of the BM6 integration.

## Overview

The `config/` directory provides a minimal Home Assistant configuration specifically designed for:
- Local development and testing
- Integration debugging
- Development environment setup
- CI/CD testing workflows

This is **not** the configuration end-users would use in their production Home Assistant instances. Instead, it's a development-only configuration that enables developers to test the BM6 integration in isolation.

---

## Files

### `configuration.yaml`

**File:** `config/configuration.yaml`

The main Home Assistant configuration file for the development environment.

#### Structure

```yaml
# https://www.home-assistant.io/integrations/default_config/
default_config:

# https://www.home-assistant.io/integrations/homeassistant/
homeassistant:
  debug: true

# https://www.home-assistant.io/integrations/logger/
logger:
  default: info
  logs:
    custom_components.bm6: debug
```

#### Configuration Components

##### 1. Default Config
```yaml
default_config:
```

**Purpose:** Loads Home Assistant's default configuration bundle.

**What It Includes:**
The `default_config` integration automatically loads a curated set of integrations that provide basic Home Assistant functionality:
- **frontend** - Web UI interface
- **config** - Configuration UI
- **http** - HTTP server for web interface
- **automation** - Automation engine
- **script** - Script execution
- **scene** - Scene management
- **zone** - Zone tracking
- **person** - Person entity tracking
- **logbook** - Event history
- **history** - State history tracking
- **map** - Map display
- **sun** - Sun position calculation
- **system_health** - System health monitoring
- **energy** - Energy management
- And many more...

**Why Use It:**
- Provides a complete Home Assistant environment with minimal configuration
- Includes all necessary components for UI access and basic functionality
- Saves time by not having to manually configure each component
- Ensures consistency across development environments

**Documentation:** [Home Assistant Default Config](https://www.home-assistant.io/integrations/default_config/)

##### 2. Home Assistant Core Settings
```yaml
homeassistant:
  debug: true
```

**Purpose:** Configures Home Assistant core behavior.

**debug: true**
- Enables debug mode for Home Assistant core
- Provides more detailed error messages and stack traces
- Helpful for troubleshooting integration issues
- Adds additional logging for internal Home Assistant operations
- **Warning:** Should not be used in production as it impacts performance

**Additional Options Available** (not currently configured):
- `name` - Name of the Home Assistant instance
- `latitude/longitude` - Geographic location
- `elevation` - Altitude in meters
- `unit_system` - metric or imperial
- `time_zone` - Timezone (e.g., "America/New_York")
- `allowlist_external_dirs` - Directories accessible by Home Assistant
- `external_url` - External URL for the instance
- `internal_url` - Internal URL for the instance

**Documentation:** [Home Assistant Core Configuration](https://www.home-assistant.io/integrations/homeassistant/)

##### 3. Logger Configuration
```yaml
logger:
  default: info
  logs:
    custom_components.bm6: debug
```

**Purpose:** Controls logging verbosity for Home Assistant and components.

**default: info**
- Sets the default log level to `info` for all components
- Provides standard logging (warnings, errors, important info)
- Balances between verbosity and usefulness

**Available Log Levels** (from most to least verbose):
1. `debug` - Detailed debugging information
2. `info` - General informational messages
3. `warning` - Warning messages for potential issues
4. `error` - Error messages only
5. `critical` - Critical errors only

**custom_components.bm6: debug**
- Overrides the default log level specifically for the BM6 integration
- Enables detailed debug logging for BM6 component only
- Critical for development and troubleshooting
- Shows all debug statements in the BM6 code

**Example Log Output:**
With this configuration, you'll see:
- Standard `info` level logs from Home Assistant core
- Standard `info` level logs from other integrations
- Detailed `debug` level logs from BM6 integration

**Benefits:**
- Focuses debugging on the BM6 integration
- Reduces noise from other components
- Makes it easier to trace BM6-specific issues
- Helps identify integration behavior during development

**Documentation:** [Home Assistant Logger](https://www.home-assistant.io/integrations/logger/)

---

## Usage

### Local Development Setup

#### 1. Prerequisites
- Home Assistant Core installed
- BM6 integration in `custom_components/bm6/`
- Python environment with Home Assistant dependencies

#### 2. Running Home Assistant with This Config
```bash
# From the repository root
hass -c config/
```

This command:
- Starts Home Assistant
- Uses `config/` as the configuration directory
- Loads the BM6 integration from `custom_components/`
- Enables debug logging for BM6

#### 3. Accessing the Instance
Once running:
- **Web UI:** http://localhost:8123
- **Logs:** View in terminal or `config/home-assistant.log`

#### 4. Viewing Debug Logs
Debug logs for BM6 will appear in:
- Terminal output (if running in foreground)
- `config/home-assistant.log` file
- Home Assistant UI: Settings > System > Logs

Filter for BM6-specific logs:
```bash
tail -f config/home-assistant.log | grep "custom_components.bm6"
```

### Development Workflow

#### 1. Make Code Changes
Edit files in `custom_components/bm6/`

#### 2. Restart Home Assistant
After code changes:
```bash
# Stop with Ctrl+C, then restart
hass -c config/
```

Or use the Home Assistant UI:
- Developer Tools > YAML > Restart

#### 3. Monitor Logs
Watch for debug output:
```bash
# Real-time log monitoring
tail -f config/home-assistant.log

# Filter for errors
tail -f config/home-assistant.log | grep "ERROR"

# Filter for BM6 only
tail -f config/home-assistant.log | grep "bm6"
```

#### 4. Test Integration
- Add the BM6 integration through the UI
- Configure with test battery monitor device
- Verify functionality
- Check logs for any errors or warnings

### CI/CD Testing

This configuration can also be used in automated testing:

```bash
# Start Home Assistant in background
hass -c config/ &
HASS_PID=$!

# Wait for Home Assistant to start
sleep 30

# Run integration tests
pytest tests/

# Cleanup
kill $HASS_PID
```

---

## Customization

### Adding Test Entities

You can extend the configuration for testing specific scenarios:

```yaml
# configuration.yaml

default_config:

homeassistant:
  debug: true

logger:
  default: info
  logs:
    custom_components.bm6: debug

# Add test sensors
sensor:
  - platform: template
    sensors:
      test_battery_voltage:
        friendly_name: "Test Battery Voltage"
        value_template: "12.6"
        unit_of_measurement: "V"

# Add test automation
automation:
  - alias: "Test BM6 Automation"
    trigger:
      - platform: state
        entity_id: sensor.bm6_voltage
    action:
      - service: notify.persistent_notification
        data:
          message: "BM6 voltage changed"
```

### Adjusting Log Levels

**More Verbose Logging:**
```yaml
logger:
  default: debug  # Enable debug for everything
  logs:
    custom_components.bm6: debug
```

**Less Verbose Logging:**
```yaml
logger:
  default: warning  # Only warnings and errors
  logs:
    custom_components.bm6: info  # Still show BM6 info
```

**Multiple Component Debugging:**
```yaml
logger:
  default: info
  logs:
    custom_components.bm6: debug
    homeassistant.components.bluetooth: debug
    homeassistant.components.mqtt: debug
```

### Adding Location Data

```yaml
homeassistant:
  debug: true
  name: "BM6 Development"
  latitude: 40.7128
  longitude: -74.0060
  elevation: 10
  unit_system: metric
  time_zone: "America/New_York"
```

### Enabling Additional Integrations

```yaml
default_config:

homeassistant:
  debug: true

logger:
  default: info
  logs:
    custom_components.bm6: debug

# Enable MQTT for testing
mqtt:
  broker: localhost
  port: 1883

# Enable Bluetooth
bluetooth:

# Enable recorder for history
recorder:
  db_url: sqlite:///config/test.db
```

---

## Troubleshooting

### Home Assistant Won't Start

**Check Configuration Syntax:**
```bash
hass -c config/ --script check_config
```

**Common Issues:**
- YAML indentation errors (use spaces, not tabs)
- Missing required dependencies
- Port 8123 already in use

### No Debug Logs Appearing

**Verify Logger Configuration:**
- Check YAML indentation under `logger:`
- Ensure `custom_components.bm6: debug` is properly indented
- Restart Home Assistant after changes

**Check Component Name:**
```bash
# Verify the integration is in the correct location
ls custom_components/bm6/
```

### Integration Not Loading

**Check Integration Structure:**
```bash
custom_components/bm6/
├── __init__.py
├── manifest.json
├── config_flow.py
└── ...
```

**View Integration Errors:**
```bash
tail -f config/home-assistant.log | grep -E "(ERROR|WARNING).*bm6"
```

**Enable Even More Verbose Logging:**
```yaml
logger:
  default: info
  logs:
    custom_components.bm6: debug
    homeassistant.loader: debug  # Shows integration loading
    homeassistant.setup: debug   # Shows setup process
```

### Port Already in Use

If port 8123 is already in use:
```yaml
http:
  server_port: 8124
```

---

## Best Practices

### 1. Keep Configuration Minimal
- Only include settings necessary for testing
- Avoid adding production-specific configurations
- Focus on enabling debugging and development features

### 2. Document Custom Changes
If adding test-specific configurations:
```yaml
# Test automation for voltage monitoring
automation:
  - alias: "Test BM6 Voltage Alert"
    # ... configuration
```

### 3. Version Control
- Commit this configuration to the repository
- Ensures consistent development environment
- Helps new developers get started quickly

### 4. Separate from Production
- Never use this configuration in production
- Keep separate from personal Home Assistant instance
- Use dedicated development directory

### 5. Regular Updates
- Keep Home Assistant version up-to-date
- Test integration against latest stable release
- Update configuration for deprecated options

### 6. Security Considerations
- Debug mode exposes internal details
- Don't expose development instance to internet
- Use localhost/internal network only
- Don't commit secrets or API keys

---

## Directory Structure

Typical `config/` directory contents during development:

```
config/
├── configuration.yaml          # Main configuration (tracked in git)
├── .storage/                   # Runtime storage (not tracked)
├── home-assistant.log          # Log file (not tracked)
├── home-assistant_v2.db        # Database (not tracked)
├── deps/                       # Dependencies (not tracked)
└── custom_components/          # Usually symlinked to ../custom_components
```

### What to Git Ignore

Add to `.gitignore`:
```
config/.storage/
config/home-assistant.log*
config/home-assistant_v2.db*
config/deps/
config/*.db
config/*.db-*
```

### What to Commit

Commit to git:
- `configuration.yaml` - The base configuration
- Any custom test configurations
- Documentation about the configuration

---

## Alternative Testing Approaches

### 1. Docker Container
```bash
docker run -d \
  --name homeassistant-dev \
  -v $(pwd)/config:/config \
  -v $(pwd)/custom_components:/config/custom_components \
  -p 8123:8123 \
  ghcr.io/home-assistant/home-assistant:stable
```

### 2. Home Assistant Container
```bash
# Using official Home Assistant Container
docker run --rm \
  -v $(pwd)/config:/config \
  homeassistant/home-assistant:latest \
  python -m homeassistant -c /config --script check_config
```

### 3. Development Container (VS Code)
Create `.devcontainer/devcontainer.json`:
```json
{
  "name": "Home Assistant Dev",
  "image": "ghcr.io/home-assistant/devcontainer:latest",
  "postCreateCommand": "pip install -e ."
}
```

---

## Related Links

- [Home Assistant Configuration Documentation](https://www.home-assistant.io/docs/configuration/)
- [Default Config Integration](https://www.home-assistant.io/integrations/default_config/)
- [Logger Integration](https://www.home-assistant.io/integrations/logger/)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Integration Development Guide](https://developers.home-assistant.io/docs/creating_integration_manifest)
- [Testing Integrations](https://developers.home-assistant.io/docs/development_testing)
