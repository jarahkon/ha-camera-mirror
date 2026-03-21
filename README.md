# ha-tablet-mirror

A self-contained mirror feature for Home Assistant dashboards. Opens the tablet's front camera as a mirror with automatic face detection — if no face is detected for 60 seconds, it returns to the dashboard automatically.

Designed for **Samsung tablets** running **Fully Kiosk Browser**.

## Features

- **Front camera mirror** — uses `getUserMedia` with `facingMode: "user"`, horizontally flipped via CSS
- **Face detection** — uses the native Chromium `FaceDetector` API (available in Fully Kiosk Browser's WebView)
- **Motion detection fallback** — if `FaceDetector` API is unavailable, falls back to frame-differencing motion detection
- **Auto-exit** — returns to dashboard after 60 seconds with no face/motion detected (shows countdown in last 10s)
- **Exit button** — manual close button (top-right corner)
- **Screen wake lock** — prevents the screen from sleeping while the mirror is active
- **Fully Kiosk Browser integration** — uses `fully.loadStartUrl()` when available for seamless return
- **Zero dependencies** — single self-contained HTML file, no external libraries or CDN

## Quick Start

### 1. Deploy `mirror.html` to Home Assistant

Copy `www/mirror.html` to your Home Assistant's `/config/www/` folder. Choose one method:

**Option A: File Editor Add-on (easiest)**
1. Install the **File Editor** add-on from **Settings → Add-ons → Add-on Store**
2. Open the File Editor
3. Navigate to the `/config/www/` folder (create `www` folder if it doesn't exist)
4. Create a new file named `mirror.html`
5. Paste the contents of [`www/mirror.html`](www/mirror.html)

**Option B: Samba Share Add-on**
1. Install the **Samba share** add-on from **Settings → Add-ons → Add-on Store**
2. Access the share from your computer: `\\homeassistant.local\config\www\`
3. Copy `www/mirror.html` into the `www` folder

**Option C: SSH Add-on**
1. Install the **SSH & Web Terminal** add-on
2. Connect via SSH and copy the file:
   ```bash
   mkdir -p /config/www
   # Copy or create mirror.html in /config/www/
   ```

### 2. Add the Mirror Button to Your Dashboard

1. Open your Home Assistant dashboard
2. Click the three-dot menu → **Edit Dashboard**
3. Click **+ Add Card** → choose **Button**
4. Switch to **YAML mode** (Show Code Editor)
5. Paste this configuration:

```yaml
type: button
name: "🪞 Mirror"
icon: mdi:mirror
tap_action:
  action: url
  url_path: /local/mirror.html
show_name: true
show_icon: true
icon_height: 60px
```

6. Save

### 3. Fully Kiosk Browser Settings

In Fully Kiosk Browser settings on your tablet:

1. **Web Content Settings → Enable JavaScript**: ON
2. **Web Content Settings → Autoplay Videos**: ON
3. **Advanced Web Settings → Enable Webcam Access (PLUS)**: ON
4. **Advanced Web Settings → Webcam/Microphone Access without prompt**: ON (recommended)
5. **Device Management → Keep Screen On**: ON

## Configuration

The mirror page accepts a query parameter to customize the return dashboard:

```
/local/mirror.html?dashboard=/lovelace/my-tablet
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
5. **Exit**: Navigates back via Fully Kiosk's `loadStartUrl()` API or standard `window.location.href`

## Troubleshooting

### Camera doesn't work / "Camera Access Required" error
- Home Assistant runs on HTTP (not HTTPS). Standard browsers block `getUserMedia` on insecure origins.
- **Fully Kiosk Browser** bypasses this restriction when **Enable Webcam Access** is turned on (requires PLUS license).
- If using a regular browser for testing, access via `https://` or `localhost`.

### FaceDetector API not available (fallback to motion detection)
- The native `FaceDetector` API requires Chromium 70+ with the Shape Detection API enabled.
- On Android WebView (Fully Kiosk), this may not be available — the mirror will automatically fall back to motion detection.
- Motion detection works well for mirror use (any movement counts as "presence").

### Mirror closes too quickly
- Increase `noFaceTimeoutSec` in the CONFIG section of `mirror.html`.
- If using motion detection fallback and standing very still, small movements (breathing, swaying) should still be detected.

### Button opens in new tab instead of same window
- In Fully Kiosk Browser, ensure **Open URLs in New Tab** is OFF in Web Content Settings.
- If this persists, change the button card's tap_action to use JavaScript navigation by installing the `card-mod` HACS integration.

### File not found at /local/mirror.html
- Ensure the file is in `/config/www/mirror.html` (not `/config/www/www/mirror.html`).
- The `www` folder must exist inside the HA config directory.
- After adding the file, refresh the browser — no HA restart needed.

## File Structure

```
www/
  mirror.html          # Deploy this to /config/www/ on Home Assistant
dashboard-card.yaml    # Button card YAML (with card-mod styling)
dashboard-card-simple.yaml  # Button card YAML (no extra dependencies)
```
