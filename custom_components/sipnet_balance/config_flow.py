from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL


class SipnetConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SIPNET Balance."""

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Basic validation could be added here (test login)
            user_input.setdefault("scan_interval", DEFAULT_SCAN_INTERVAL)
            return self.async_create_entry(
                title="SIPNET Balance",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required("sipuid"): str,
                vol.Required("password"): str,
                vol.Optional("scan_interval", default=DEFAULT_SCAN_INTERVAL): int,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_import(self, user_input=None):
        # Not used but required by some flows
        return await self.async_step_user(user_input)


class SipnetOptionsFlow(config_entries.OptionsFlow):
    """Handle options for SIPNET Balance."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interval = self.config_entry.options.get(
            "scan_interval",
            self.config_entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL),
        )

        schema = vol.Schema(
            {
                vol.Optional("scan_interval", default=current_interval): int,
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)


async def async_get_options_flow(config_entry):
    return SipnetOptionsFlow(config_entry)
