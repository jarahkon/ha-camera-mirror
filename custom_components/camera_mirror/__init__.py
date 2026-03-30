"""Camera Mirror integration — adds a sidebar panel with a full-screen camera mirror."""

from __future__ import annotations

from pathlib import Path

from homeassistant.components.frontend import (
    async_register_built_in_panel,
    async_remove_panel,
)
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PANEL_ICON, PANEL_TITLE, PANEL_URL_PATH, URL_BASE

MIRROR_FILE = "mirror.html"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Camera Mirror from a config entry."""
    integration_dir = Path(__file__).parent
    mirror_path = str(integration_dir / MIRROR_FILE)

    # Guard against duplicate registration on setup retries.
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = True
        await hass.http.async_register_static_paths(
            [StaticPathConfig(f"{URL_BASE}/{MIRROR_FILE}", mirror_path, True)]
        )

    async_register_built_in_panel(
        hass,
        component_name="iframe",
        sidebar_title=PANEL_TITLE,
        sidebar_icon=PANEL_ICON,
        frontend_url_path=PANEL_URL_PATH,
        require_admin=False,
        config={"url": f"{URL_BASE}/{MIRROR_FILE}"},
        update=True,
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data.pop(DOMAIN, None)
    async_remove_panel(hass, PANEL_URL_PATH, warn_if_unknown=False)
    return True
