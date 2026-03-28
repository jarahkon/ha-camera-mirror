# ha-camera-mirror

[![HACS Validation](https://github.com/jarahkon/ha-camera-mirror/actions/workflows/hacs.yml/badge.svg)](https://github.com/jarahkon/ha-camera-mirror/actions/workflows/hacs.yml)
[![Hassfest Validation](https://github.com/jarahkon/ha-camera-mirror/actions/workflows/hassfest.yml/badge.svg)](https://github.com/jarahkon/ha-camera-mirror/actions/workflows/hassfest.yml)

A Home Assistant integration that adds a full-screen camera mirror to your sidebar. Opens the device's front camera with automatic motion detection — if no motion is detected for 60 seconds, it exits automatically.

Works on any device (tablet, phone, PC) via standard `getUserMedia`. **Requires HTTPS.**

## Features

- **Sidebar panel** — appears alongside HACS, Map, etc. in the Home Assistant sidebar
- **Front camera mirror** — uses `getUserMedia` with `facingMode: "user"`, horizontally flipped via CSS
- **Motion detection** — uses frame-differencing to detect presence
- **Auto-exit** — returns to dashboard after 60 seconds with no motion detected (countdown in last 10s)
- **Exit button** — manual close button (top-right corner)
- **Screen wake lock** — prevents the screen from sleeping while the mirror is active
- **Zero dependencies** — single self-contained HTML file, no external libraries
- **HACS compatible** — install and update via HACS

## Installation

### Prerequisites

- Home Assistant 2024.1.0 or newer
- [HACS](https://hacs.xyz/) installed (recommended) or manual install
- **HTTPS enabled** on Home Assistant (camera access requires a secure context). See the [Home Assistant HTTPS documentation](https://www.home-assistant.io/docs/configuration/securing/) for setup instructions.

### Install via HACS (recommended)

1. Open HACS in your Home Assistant
2. Click the three dots menu (top right) → **Custom repositories**
3. Add `https://github.com/jarahkon/ha-camera-mirror` with category **Integration**
4. Search for "Camera Mirror" in HACS and click **Download**
5. **Restart Home Assistant**
6. Go to **Settings → Devices & Services → Add Integration → Camera Mirror**
7. Click **Submit** — "Mirror" appears in your sidebar

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jarahkon&repository=ha-camera-mirror&category=integration)

### Manual Installation

1. Copy the `custom_components/camera_mirror` directory to your Home Assistant's `custom_components/` folder
2. **Restart Home Assistant**
3. Go to **Settings → Devices & Services → Add Integration → Camera Mirror**
4. Click **Submit** — "Mirror" appears in your sidebar

### Browser Configuration

**Fully Kiosk Browser** (tablet):
1. Update Start URL to `https://homeassistant.local:8123`
2. **Advanced Web Settings → Enable Webcam Access (PLUS)**: ON
3. **Advanced Web Settings → Webcam/Microphone Access without prompt**: ON

## Configuration

The mirror page accepts a `dashboard` query parameter for the exit destination:

```
/camera_mirror/mirror.html?dashboard=/full-overview/0
```

Default return path is `/lovelace/0`.

### Configurable Constants (in mirror.html)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `inactivityTimeoutSec` | `60` | Seconds without motion before auto-exit |
| `detectionIntervalMs` | `1000` | Motion detection check interval (ms) |
| `motionThreshold` | `30` | Pixel difference threshold for motion detection |
| `motionPixelRatio` | `0.01` | Fraction of changed pixels to count as presence |
| `dashboardPath` | `/lovelace/0` | Dashboard path to return to |

### Optional: Dashboard Button Card

If you also want a button card on a dashboard to open the mirror, you can use the example YAML in `dashboard-card.yaml` or `dashboard-card-simple.yaml`.

## UI Indicators

| Indicator | Meaning |
|-----------|---------|
| Green dot (top-left) | Motion detected |
| Red dot (top-left) | No motion detected |
| ✕ button (top-right) | Exit mirror manually |
| Bottom status bar | Countdown warning (last 10 seconds) |

## How It Works

1. **Camera Access**: Opens front camera via `navigator.mediaDevices.getUserMedia()` with `facingMode: "user"`
2. **Mirror Effect**: Video is flipped horizontally with CSS `transform: scaleX(-1)`
3. **Motion Detection**: Compares consecutive video frames to detect presence via pixel differencing
4. **Auto-Exit Timer**: Starts a 60-second countdown when no motion is detected; resets when motion reappears
5. **Exit**: Navigates back via `history.back()` or falls back to the configured dashboard path

## Troubleshooting

### Camera doesn't work / "HTTPS Required"
- `getUserMedia` requires a secure context (HTTPS or localhost)
- Verify you're accessing HA via `https://`

### Mirror closes too quickly
- Increase `inactivityTimeoutSec` in the CONFIG section of `mirror.html`

### Mirror doesn't appear in sidebar
- Make sure you added the integration via **Settings → Devices & Services → Add Integration → Camera Mirror**
- Restart Home Assistant if needed

## File Structure

```
custom_components/
  camera_mirror/
    __init__.py        # Integration setup — registers sidebar panel
    config_flow.py     # Config flow — zero-config, just click Submit
    const.py           # Constants (domain, URLs, panel config)
    manifest.json      # Integration manifest for HA + HACS
    mirror.html        # The mirror app (self-contained HTML)
    strings.json       # UI strings
    translations/
      en.json          # English translations
    brand/
      icon.png         # Integration icon
      logo.png         # Integration logo
hacs.json              # HACS repository manifest
dashboard-card.yaml    # Optional: button card with card_mod styling
dashboard-card-simple.yaml  # Optional: simple button card
```

## License

This project is licensed under the [MIT License](LICENSE).
