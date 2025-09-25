# MAC-Based Targeted Firmware Updates

This directory contains MAC address-specific firmware update configurations for individual EVSEPARKER devices.

## How it Works

1. **Customer Issues**: When a specific customer reports an issue that requires a custom firmware fix
2. **Target Creation**: Create a JSON file named after their MAC address (with underscores instead of colons)
3. **Firmware Upload**: Upload the targeted firmware to the appropriate directory
4. **Customer Access**: Customer enters their MAC address on the main page to access their specific update

## File Naming Convention

- **MAC Address**: `AB:CD:EF:12:34:56` becomes `AB_CD_EF_12_34_56.json`
- **Firmware Files**: Store in `/targeted/firmware/[MAC]/` directory

## Example Targeted Update

### File: `AB_CD_EF_12_34_56.json`
```json
{
  "customer_info": {
    "mac_address": "AB:CD:EF:12:34:56",
    "device_serial": "EVSE-2024-001234",
    "customer_name": "John Doe",
    "issue_ticket": "SUPPORT-2024-789",
    "created_date": "2024-09-25T12:00:00Z"
  },
  "devices": [
    {
      "model": "EVSEPARKER_V2_GEN2",
      "latest_version": "10.2.1-custom",
      "url": "https://demirciberkan.github.io/targeted/firmware/AB_CD_EF_12_34_56/EVSE_10_2_1_custom.bin",
      "changelog": "TARGETED FIX: Resolves specific relay timing issue for this device. Custom calibration values for temperature sensor.",
      "release_date": "2024-09-25T12:00:00Z",
      "file_size": "1.16 MB",
      "hardware_version": "V2 GEN2",
      "targeted_fix": true,
      "fix_description": [
        "Custom relay timing parameters for reported intermittent switching issue",
        "Adjusted temperature sensor calibration for reported high readings",
        "Increased GFCI test timeout for this specific hardware batch"
      ],
      "rollback_info": {
        "stable_version": "10.2.0",
        "stable_url": "https://demirciberkan.github.io/firmware/EVSEPARKER_V2_GEN2/EVSE_10_2_0.bin"
      },
      "security": {
        "signed": true,
        "checksum": "sha256:custom123456..."
      }
    }
  ],
  "instructions": {
    "installation": [
      "1. Download the custom firmware using the EVSEPARKER mobile app",
      "2. Ensure device is connected to power and not actively charging",
      "3. Initiate OTA update through the app",
      "4. Wait for automatic reboot and verification",
      "5. Test the specific functionality that was reported as problematic"
    ],
    "verification": [
      "Check that relay switching is now consistent",
      "Verify temperature readings are within expected range",
      "Test GFCI functionality with longer timeout"
    ],
    "support_contact": "berkan@demirciberkan.com"
  },
  "expiry_date": "2024-12-25T00:00:00Z",
  "auto_rollback": false
}
```

## Directory Structure

```
targeted/
├── README.md                           # This file
├── AB_CD_EF_12_34_56.json             # Targeted config for specific MAC
├── firmware/
│   └── AB_CD_EF_12_34_56/              # Firmware files for this MAC
│       └── EVSE_10_2_1_custom.bin      # Custom firmware binary
└── tools/
    ├── create_target.py                # Script to create targeted configs
    └── validate_target.json            # Validation script
```

## Security Considerations

1. **Access Control**: Targeted updates are only accessible with exact MAC address match
2. **Expiry Dates**: Set expiry dates for targeted updates to ensure customers don't use outdated fixes
3. **Rollback**: Always provide rollback information to stable firmware
4. **Validation**: Validate MAC addresses and ensure they correspond to known customers
5. **Audit Trail**: Log all targeted firmware accesses for security monitoring

## Best Practices

1. **Documentation**: Always document the specific issue being addressed
2. **Testing**: Thoroughly test targeted firmware before deployment
3. **Communication**: Notify customer when targeted update is available
4. **Follow-up**: Confirm fix worked and consider integrating into main firmware
5. **Cleanup**: Remove targeted updates once issue is resolved in main firmware

## Management Commands

```bash
# Create new targeted update
./tools/create_target.py --mac "AB:CD:EF:12:34:56" --issue "SUPPORT-2024-789" --version "10.2.1-custom"

# List all active targeted updates
ls *.json

# Check expiry dates
./tools/validate_target.py --check-expiry

# Clean up expired targets
./tools/cleanup_expired.py
```

## Support Workflow

1. **Issue Reported**: Customer reports specific hardware issue
2. **Investigation**: Engineering team identifies need for custom firmware
3. **Target Creation**: Create targeted update configuration
4. **Firmware Build**: Build custom firmware with specific fixes
5. **Deployment**: Upload firmware and notify customer
6. **Testing**: Customer tests and reports results
7. **Integration**: If successful, integrate fix into main firmware
8. **Cleanup**: Remove targeted update after integration

## Monitoring

- Monitor targeted update downloads and success rates
- Track customer feedback on targeted fixes
- Identify patterns that might indicate broader issues
- Maintain audit logs of all targeted update activities