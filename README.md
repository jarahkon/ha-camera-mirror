# ha-tablet-mirror

A self-contained mirror app for Home Assistant. Opens the device's front camera as a full-screen mirror with automatic face/motion detection — if no one is detected for 60 seconds, it exits automatically.

Works on any device (tablet, phone, PC) via standard `getUserMedia`. **Requires HTTPS.**

## Features

- **Front camera mirror** — uses `getUserMedia` with `facingMode: "user"`, horizontally flipped via CSS
- **Face detection** — uses the native Chromium `FaceDetector` API when available
- **Motion detection fallback** — falls back to frame-differencing motion detection automatically
- **Auto-exit** — returns to dashboard after 60 seconds with no face/motion detected (countdown in last 10s)
- **Exit button** — manual close button (top-right corner)
- **Screen wake lock** — prevents the screen from sleeping while the mirror is active
- **Zero dependencies** — single self-contained HTML file, no external libraries

## Setup

### Prerequisites

- Home Assistant with **HTTPS enabled** (camera access requires a secure context)
- SSL certificate files in `/config/ssl/` (see [HTTPS Setup](#1-enable-https-on-home-assistant))

### 1. Enable HTTPS on Home Assistant

Generate a self-signed certificate (or use Let's Encrypt):

```bash
# Generate cert files (from this repo)
python gen_cert.py
```

This creates `ssl/fullchain.pem` and `ssl/privkey.pem` with SANs for `homeassistant.local` and your HA IP.

Upload the cert files to Home Assistant:

```bash
# Via Samba, SSH, or File Editor add-on:
mkdir -p /config/ssl
# Copy ssl/fullchain.pem → /config/ssl/fullchain.pem
# Copy ssl/privkey.pem  → /config/ssl/privkey.pem
```

Add to `configuration.yaml`:

```yaml
http:
  ssl_certificate: /ssl/fullchain.pem
  ssl_key: /ssl/privkey.pem
```

### 2. Deploy mirror.html

Copy `www/mirror.html` to `/config/www/mirror.html` on Home Assistant.

### 3. Add Mirror to Sidebar

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

### 4. Restart Home Assistant

Restart HA for the HTTPS changes to take effect.

### 5. Browser Configuration

**Fully Kiosk Browser** (tablet):
1. Update Start URL to `https://homeassistant.local:8123`
2. **Advanced Web Settings → Ignore SSL Errors**: ON (for self-signed cert)
3. **Advanced Web Settings → Enable Webcam Access (PLUS)**: ON
4. **Advanced Web Settings → Webcam/Microphone Access without prompt**: ON

**Desktop browsers**: Accept the self-signed certificate warning on first visit.

## Configuration

The mirror page accepts a `dashboard` query parameter for the exit destination:

```
/local/mirror.html?dashboard=/full-overview/0
```

Default return path is `/lovelace/0`.

### Configurable Constants (in mirror.html)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `noFaceTimeoutSec` | `60` | Seconds without face before auto-exit |
| `detectionIntervalMs` | `1000` | Face detection check interval (ms) |
| `motionThreshold` | `15` | Pixel difference threshold for motion fallback |
| `motionPixelRatio` | `0.02` | Fraction of changed pixels to count as presence |
| `dashboardPath` | `/lovelace/0` | Dashboard path to return to |

## UI Indicators

| Indicator | Meaning |
|-----------|---------|
| Green dot (top-left) | Face/motion detected |
| Red dot (top-left) | No face/motion detected |
| ✕ button (top-right) | Exit mirror manually |
| Bottom status bar | Countdown warning (last 10 seconds) |

## How It Works

1. **Camera Access**: Opens front camera via `navigator.mediaDevices.getUserMedia()` with `facingMode: "user"`
2. **Mirror Effect**: Video is flipped horizontally with CSS `transform: scaleX(-1)`
3. **Face Detection**: Attempts native `FaceDetector` API first (Chromium 70+), falls back to motion detection
4. **Auto-Exit Timer**: Starts a 60-second countdown when no face is detected; resets when a face reappears
5. **Exit**: Navigates back via `history.back()` or falls back to the configured dashboard path

## Troubleshooting

### Camera doesn't work / "HTTPS Required"
- `getUserMedia` requires a secure context (HTTPS or localhost)
- Ensure the `http:` section in `configuration.yaml` has correct SSL paths
- Verify you're accessing HA via `https://`

### Self-signed certificate warnings
- Desktop: Click through the browser warning to accept the cert
- Fully Kiosk: Enable **Ignore SSL Errors** in Advanced Web Settings

### FaceDetector fallback to motion detection
- The native `FaceDetector` API requires Chromium 70+ with Shape Detection API
- Motion detection works well for mirror use — any movement counts as "presence"

### Mirror closes too quickly
- Increase `noFaceTimeoutSec` in the CONFIG section of `mirror.html`

## File Structure

```
www/
  mirror.html    # Deploy to /config/www/ on Home Assistant
ssl/
  fullchain.pem  # Generated SSL certificate
  privkey.pem    # Generated SSL private key
gen_cert.py      # Certificate generation script
```
