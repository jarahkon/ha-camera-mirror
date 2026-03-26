# ha-camera-mirror

A self-contained mirror app for Home Assistant. Opens the device's front camera as a full-screen mirror with automatic motion detection — if no motion is detected for 60 seconds, it exits automatically.

Works on any device (tablet, phone, PC) via standard `getUserMedia`. **Requires HTTPS.**

## Features

- **Front camera mirror** — uses `getUserMedia` with `facingMode: "user"`, horizontally flipped via CSS
- **Motion detection** — uses frame-differencing to detect presence
- **Auto-exit** — returns to dashboard after 60 seconds with no motion detected (countdown in last 10s)
- **Exit button** — manual close button (top-right corner)
- **Screen wake lock** — prevents the screen from sleeping while the mirror is active
- **Zero dependencies** — single self-contained HTML file, no external libraries

## Setup

### Prerequisites

- Home Assistant with **HTTPS enabled** (camera access requires a secure context). See the [Home Assistant HTTPS documentation](https://www.home-assistant.io/docs/configuration/securing/) for setup instructions.

### 1. Deploy mirror.html

Copy `www/mirror.html` to `/config/www/mirror.html` on Home Assistant.

### 2. Add Mirror to Sidebar

Create a new dashboard in HA:
1. Go to **Settings → Dashboards → Add Dashboard**
2. Set Title: `Mirror`, Icon: `mdi:mirror`
3. Enable **Show in sidebar**
4. Open the new Mirror dashboard, edit it
5. Switch to YAML mode and paste:

```yaml
views:
  - title: Mirror
    panel: true
    cards:
      - type: iframe
        url: /local/mirror.html
        aspect_ratio: "100%"
```

### 3. Browser Configuration

**Fully Kiosk Browser** (tablet):
1. Update Start URL to `https://homeassistant.local:8123`
2. **Advanced Web Settings → Enable Webcam Access (PLUS)**: ON
3. **Advanced Web Settings → Webcam/Microphone Access without prompt**: ON

## Configuration

The mirror page accepts a `dashboard` query parameter for the exit destination:

```
/local/mirror.html?dashboard=/full-overview/0
```

Default return path is `/lovelace/0`.

### Configurable Constants (in mirror.html)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `inactivityTimeoutSec` | `60` | Seconds without motion before auto-exit |
| `detectionIntervalMs` | `1000` | Motion detection check interval (ms) |
| `motionThreshold` | `15` | Pixel difference threshold for motion detection |
| `motionPixelRatio` | `0.02` | Fraction of changed pixels to count as presence |
| `dashboardPath` | `/lovelace/0` | Dashboard path to return to |

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

## File Structure

```
www/
  mirror.html    # Deploy to /config/www/ on Home Assistant
```
