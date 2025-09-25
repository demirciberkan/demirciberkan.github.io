# EVSEPARKER Firmware Distribution Hub

A comprehensive web platform for EVSEPARKER electric vehicle charging equipment, featuring firmware distribution, web-based device control, and OTA update management.

## 🌟 Features

- **Firmware Distribution**: Centralized repository for all EVSEPARKER firmware versions
- **Web Bluetooth Control**: Direct device control through modern web browsers
- **OTA Update System**: Over-the-air firmware updates via mobile app
- **Beta Testing Portal**: Secure access to pre-release firmware builds
- **Multi-Hardware Support**: Support for different hardware generations (V2 GEN1, V2 GEN2)
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 📁 Website Structure

```
demirciberkan.github.io/
├── index.html              # Web Bluetooth control interface
├── firmware-index.html     # Main firmware distribution page
├── manifest.json           # Stable firmware manifest
├── README.md              # This documentation
├── firmware/              # Stable firmware files
│   ├── EVSEPARKER_V2_GEN1/
│   └── EVSEPARKER_V2_GEN2/
└── testing/               # Beta testing portal
    ├── index.html         # Beta testing interface
    ├── manifest.json      # Testing firmware manifest
    └── firmware/          # Beta firmware files
        ├── EVSEPARKER_V2_GEN1/
        └── EVSEPARKER_V2_GEN2/
```

## 🚀 Quick Start

### For End Users

1. **Web Control**: Visit `index.html` to control your EVSEPARKER device via Web Bluetooth
2. **Firmware Updates**: Visit `firmware-index.html` to download the latest stable firmware
3. **Mobile OTA**: Use the EVSEPARKER mobile app for wireless firmware updates

### For Developers/Beta Testers

1. **Beta Access**: Visit `testing/index.html` for pre-release firmware builds
2. **Safety First**: Always read the testing guidelines before using beta firmware
3. **Bug Reports**: Use the provided links to report issues with beta builds

## 📦 Firmware Management

### Stable Release Process

1. Update `manifest.json` with new firmware information:
   ```json
   {
     "devices": [
       {
         "model": "EVSEPARKER_V2_GEN2",
         "latest_version": "10.2.0",
         "url": "https://demirciberkan.github.io/firmware/EVSEPARKER_V2_GEN2/EVSE_10_2_0.bin",
         "changelog": "Your release notes here",
         "release_date": "2024-09-25T00:00:00Z",
         "file_size": "1.15 MB"
       }
     ]
   }
   ```

2. Upload firmware binary to `firmware/[MODEL]/` directory

3. Test the download and OTA functionality

### Beta Release Process

1. Update `testing/manifest.json` with beta firmware information
2. Upload beta firmware to `testing/firmware/[MODEL]/` directory
3. Notify beta testers of new builds available
4. Monitor for feedback and bug reports

## 🔧 Hardware Support

### EVSEPARKER_V2_GEN1
- **Description**: Original V2 hardware revision
- **Pin Configuration**: Standard pin assignments
- **Features**: Multi-phase monitoring, GFCI protection, temperature sensing

### EVSEPARKER_V2_GEN2
- **Description**: Second generation V2 hardware
- **Pin Changes**:
  - Relay pin: GPIO 14 (was GPIO 27)
  - Buzzer pin: GPIO 2 (was GPIO 19)
- **Features**: All GEN1 features + improved relay control

## 🛡️ Security Considerations

### Firmware Integrity
- All firmware builds should include checksums
- Consider implementing firmware signing for production builds
- Monitor download statistics and detect anomalies

### Access Control
- Beta testing portal should have restricted access
- Consider implementing authentication for beta downloads
- Monitor and log all firmware download activity

### Safety Requirements
- Never deploy untested firmware to production devices
- Always provide rollback procedures
- Include safety warnings on beta firmware

## 📱 Web Bluetooth Interface

The main web interface (`index.html`) provides:

- **Device Connection**: Scan and connect to EVSEPARKER devices
- **Real-time Monitoring**: Power, current, energy, temperature readings
- **Settings Management**: Configure charging parameters and safety settings
- **PIN Management**: Change device security PIN
- **OTA Information**: Access firmware update information

### Browser Compatibility

- ✅ Chrome/Chromium (recommended)
- ✅ Microsoft Edge
- ❌ Firefox (Web Bluetooth not supported)
- ❌ Safari (Web Bluetooth not supported)

## 🔄 OTA Update Flow

1. **Mobile App**: User initiates OTA update through EVSEPARKER mobile app
2. **Manifest Check**: App fetches latest manifest.json for available updates
3. **Download**: App downloads appropriate firmware for device model
4. **Transfer**: Firmware transferred to device via BLE OTA protocol
5. **Installation**: Device validates and installs new firmware
6. **Restart**: Device reboots with new firmware

## 🧪 Beta Testing Guidelines

### Safety Requirements
- ⚠️ Test with no live electrical connections initially
- ⚠️ Use current-limited power supply for testing
- ⚠️ Have emergency stop procedures in place
- ⚠️ Never leave testing firmware unattended during charging

### Testing Process
1. Download beta firmware from testing portal
2. Review known issues and testing features
3. Install firmware using mobile app OTA
4. Perform required tests (minimum 24 hours)
5. Document any issues or unexpected behavior
6. Report findings through provided channels

### Reporting Requirements
- Hardware revision and serial number
- Firmware version and build date
- Test conditions and environment
- Step-by-step reproduction instructions
- Serial console logs (if available)

## 🔧 Development Setup

### Local Development
```bash
# Clone the repository
git clone https://github.com/demirciberkan/demirciberkan.github.io.git

# Serve locally (Python)
cd demirciberkan.github.io
python -m http.server 8000

# Or using Node.js
npx http-server .
```

### Firmware Build Process
```bash
# Arduino CLI example
arduino-cli compile --fqbn esp32:esp32:esp32 EVSE_10_1_OTA.ino
arduino-cli compile --export-binaries --fqbn esp32:esp32:esp32 EVSE_10_1_OTA.ino
```

## 📊 Analytics & Monitoring

### Recommended Tracking
- Firmware download counts by version/model
- Web Bluetooth connection success rates
- OTA update success/failure rates
- Beta testing participation metrics
- Browser compatibility statistics

### Logs to Monitor
- Failed firmware downloads
- Web Bluetooth connection errors
- OTA update failures
- Beta firmware crash reports

## 🚀 Deployment

### GitHub Pages Setup
1. Repository must be named `username.github.io`
2. Ensure all paths are relative or absolute GitHub Pages URLs
3. Test all functionality after deployment
4. Monitor for CORS issues with external resources

### CDN Considerations
- Large firmware files may benefit from CDN distribution
- Consider implementing download mirrors for global users
- Monitor bandwidth usage and costs

## 📄 License

This project is part of the EVSEPARKER ecosystem. See main repository for licensing information.

## 🤝 Contributing

1. Test all changes thoroughly before deployment
2. Update documentation when adding new features
3. Follow security best practices for firmware distribution
4. Coordinate with hardware team for new device support

## 📞 Support

- **Issues**: Report bugs through GitHub Issues
- **Documentation**: Check this README and inline documentation
- **Beta Testing**: Contact beta test coordinator for access
- **Hardware Support**: Contact hardware development team

---

**⚠️ Important**: This system handles firmware distribution for safety-critical equipment. Always prioritize safety and thorough testing over rapid deployment.