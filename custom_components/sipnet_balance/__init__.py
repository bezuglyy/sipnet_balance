from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """YAML setup not used; config_flow only."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SIPNET Balance from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    # Register refresh service once
    async def handle_refresh(call: ServiceCall) -> None:
        # Refresh main sensor entity
        await hass.services.async_call(
            "homeassistant",
            "update_entity",
            {"entity_id": "sensor.sipnet_balance"},
            blocking=False,
        )

    if not hass.services.has_service(DOMAIN, "refresh"):
        hass.services.async_register(DOMAIN, "refresh", handle_refresh)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    return unload_ok
