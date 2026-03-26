"""Config flow for Camera Mirror."""

from homeassistant.config_entries import ConfigFlow

from .const import DOMAIN


class CameraMirrorConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Camera Mirror."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Camera Mirror", data={})

        return self.async_show_form(step_id="user")
