# Device Firmware Query API Example

This document shows how EVSEPARKER devices can query the manifest.json to find available firmware updates, including MAC-specific targeted updates.

## Basic Firmware Query

Devices can fetch the manifest and find compatible firmware:

```javascript
// Device queries manifest.json
async function checkForFirmwareUpdates(deviceMAC, currentVersion, hardwareModel) {
    try {
        const response = await fetch('https://demirciberkan.github.io/manifest.json');
        const manifest = await response.json();

        // Check for MAC-specific firmware first
        const macSpecific = manifest.mac_specific[deviceMAC];
        if (macSpecific && macSpecific.model === hardwareModel) {
            console.log(`Found targeted firmware for MAC ${deviceMAC}: v${macSpecific.version}`);
            return {
                hasUpdate: true,
                version: macSpecific.version,
                url: macSpecific.url,
                description: macSpecific.description,
                isTargeted: true,
                expires: macSpecific.expires
            };
        }

        // Check general firmware updates
        const modelFirmware = manifest.hardware_models[hardwareModel];
        if (modelFirmware && modelFirmware.firmware_versions.length > 0) {
            // Get latest version (first in array, as they're sorted by date)
            const latestFirmware = modelFirmware.firmware_versions[0];

            if (latestFirmware.version !== currentVersion) {
                console.log(`Found general firmware update: v${latestFirmware.version}`);
                return {
                    hasUpdate: true,
                    version: latestFirmware.version,
                    url: latestFirmware.url,
                    description: latestFirmware.description,
                    isTargeted: false,
                    releaseDate: latestFirmware.release_date
                };
            }
        }

        return { hasUpdate: false };

    } catch (error) {
        console.error('Failed to check for firmware updates:', error);
        return { hasUpdate: false, error: error.message };
    }
}

// Usage example:
const updateInfo = await checkForFirmwareUpdates(
    "AB:CD:EF:12:34:56",    // Device MAC address
    "10.1.43",              // Current firmware version
    "EVSEPARKER_V2_GEN2"    // Hardware model
);

if (updateInfo.hasUpdate) {
    console.log('Firmware update available!');
    console.log(`New version: ${updateInfo.version}`);
    console.log(`Download URL: ${updateInfo.url}`);
    console.log(`Type: ${updateInfo.isTargeted ? 'Targeted' : 'General'}`);
}
```

## Arduino/ESP32 Implementation Example

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

class FirmwareUpdater {
private:
    String deviceMAC;
    String currentVersion;
    String hardwareModel;
    const String manifestURL = "https://demirciberkan.github.io/manifest.json";

public:
    FirmwareUpdater(String mac, String version, String model)
        : deviceMAC(mac), currentVersion(version), hardwareModel(model) {}

    struct UpdateInfo {
        bool hasUpdate;
        String version;
        String url;
        String description;
        bool isTargeted;
        String error;
    };

    UpdateInfo checkForUpdates() {
        UpdateInfo result = {false, "", "", "", false, ""};

        if (WiFi.status() != WL_CONNECTED) {
            result.error = "WiFi not connected";
            return result;
        }

        HTTPClient http;
        http.begin(manifestURL);

        int httpResponseCode = http.GET();
        if (httpResponseCode != 200) {
            result.error = "HTTP error: " + String(httpResponseCode);
            http.end();
            return result;
        }

        String payload = http.getString();
        http.end();

        // Parse JSON manifest
        DynamicJsonDocument doc(8192);
        DeserializationError error = deserializeJson(doc, payload);

        if (error) {
            result.error = "JSON parse error";
            return result;
        }

        // Check for MAC-specific firmware
        if (doc["mac_specific"].containsKey(deviceMAC)) {
            JsonObject macSpecific = doc["mac_specific"][deviceMAC];
            if (macSpecific["model"] == hardwareModel) {
                result.hasUpdate = true;
                result.version = macSpecific["version"].as<String>();
                result.url = macSpecific["url"].as<String>();
                result.description = macSpecific["description"].as<String>();
                result.isTargeted = true;

                Serial.println("Found targeted firmware update!");
                return result;
            }
        }

        // Check general firmware updates
        if (doc["hardware_models"].containsKey(hardwareModel)) {
            JsonArray firmwareVersions = doc["hardware_models"][hardwareModel]["firmware_versions"];

            if (firmwareVersions.size() > 0) {
                JsonObject latestFirmware = firmwareVersions[0]; // Latest is first
                String latestVersion = latestFirmware["version"];

                if (latestVersion != currentVersion) {
                    result.hasUpdate = true;
                    result.version = latestVersion;
                    result.url = latestFirmware["url"];
                    result.description = latestFirmware["description"];
                    result.isTargeted = false;

                    Serial.println("Found general firmware update!");
                }
            }
        }

        return result;
    }
};

// Usage in your main code:
void setup() {
    Serial.begin(115200);

    // Get device MAC address
    String mac = WiFi.macAddress();

    FirmwareUpdater updater(mac, "10.1.43", "EVSEPARKER_V2_GEN2");

    // Check for updates periodically
    FirmwareUpdater::UpdateInfo updateInfo = updater.checkForUpdates();

    if (updateInfo.hasUpdate) {
        Serial.printf("Firmware update available: v%s\n", updateInfo.version.c_str());
        Serial.printf("Type: %s\n", updateInfo.isTargeted ? "Targeted" : "General");
        Serial.printf("URL: %s\n", updateInfo.url.c_str());

        // Initiate OTA update process here...
    } else if (updateInfo.error != "") {
        Serial.printf("Update check failed: %s\n", updateInfo.error.c_str());
    } else {
        Serial.println("No firmware updates available");
    }
}
```

## Mobile App Integration

For the React Native mobile app to check for MAC-specific updates:

```javascript
// In your React Native app
const checkDeviceFirmware = async (deviceMAC, currentFW, hardwareModel) => {
    try {
        const response = await fetch('https://demirciberkan.github.io/manifest.json');
        const manifest = await response.json();

        // Check MAC-specific updates first
        const targeted = manifest.mac_specific?.[deviceMAC];
        if (targeted && targeted.model === hardwareModel) {
            return {
                updateAvailable: true,
                version: targeted.version,
                url: targeted.url,
                description: targeted.description,
                isTargeted: true,
                priority: 'high' // Targeted updates are high priority
            };
        }

        // Check general updates
        const modelData = manifest.hardware_models?.[hardwareModel];
        if (modelData?.firmware_versions?.length > 0) {
            const latest = modelData.firmware_versions[0];
            if (latest.version !== currentFW) {
                return {
                    updateAvailable: true,
                    version: latest.version,
                    url: latest.url,
                    description: latest.description,
                    isTargeted: false,
                    priority: 'normal'
                };
            }
        }

        return { updateAvailable: false };
    } catch (error) {
        console.error('Firmware check failed:', error);
        return { updateAvailable: false, error: error.message };
    }
};
```

## Adding MAC-Specific Firmware

To add a targeted firmware for a specific device MAC:

1. **Add to manifest.json:**
```json
{
  "mac_specific": {
    "AB:CD:EF:12:34:56": {
      "model": "EVSEPARKER_V2_GEN2",
      "version": "10.2.1-custom-relay-fix",
      "url": "https://demirciberkan.github.io/firmware/EVSEPARKER_V2_GEN2/EVSE_10_2_1_custom_ABCDEF123456.bin",
      "description": "Custom firmware for specific relay timing issue",
      "expires": "2024-12-25"
    }
  }
}
```

2. **Upload firmware file:**
   - Place the custom firmware in the model's firmware directory
   - Use a naming convention that includes the MAC or issue identifier
   - Example: `EVSE_10_2_1_custom_ABCDEF123456.bin`

3. **Test the targeting:**
   - Device with MAC `AB:CD:EF:12:34:56` will get the custom firmware
   - All other devices get the standard firmware versions

## Security Considerations

- Always verify firmware integrity before installation
- MAC-specific updates should have expiry dates
- Log all firmware update attempts for audit purposes
- Validate that the device MAC requesting targeted firmware is authorized

## Best Practices

1. **Targeted Updates:**
   - Use only for specific customer issues
   - Include clear descriptions of what's fixed
   - Set reasonable expiry dates
   - Remove after integrating fix into main firmware

2. **Version Management:**
   - Keep firmware versions sorted by release date (newest first)
   - Use semantic versioning
   - Maintain backwards compatibility information

3. **Error Handling:**
   - Always handle network failures gracefully
   - Provide fallback mechanisms
   - Log errors for debugging

4. **Testing:**
   - Test manifest parsing with malformed JSON
   - Verify MAC address format handling
   - Test with missing network connectivity