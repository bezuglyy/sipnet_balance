from __future__ import annotations

import logging
import re
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_URL, DEFAULT_NAME, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up SIPNET Balance sensor from config entry."""
    sipuid = entry.data["sipuid"]
    password = entry.data["password"]
    scan_interval = entry.options.get(
        "scan_interval", entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL)
    )

    entity = SipnetBalanceSensor(hass, sipuid, password, scan_interval)
    async_add_entities([entity], True)


class SipnetBalanceSensor(SensorEntity):
    """Sensor for SIPNET balance."""

    _attr_icon = "mdi:currency-rub"
    _attr_native_unit_of_measurement = "₽"
    _attr_should_poll = True

    def __init__(
        self,
        hass: HomeAssistant,
        sipuid: str,
        password: str,
        scan_interval: int,
    ) -> None:
        self.hass = hass
        self._sipuid = sipuid
        self._password = password
        self._attr_name = DEFAULT_NAME
        self._attr_unique_id = f"sipnet_balance_{sipuid}"
        self._scan_interval = timedelta(seconds=int(scan_interval))
        self._attr_native_value = None

    @property
    def scan_interval(self) -> timedelta:
        return self._scan_interval

    async def async_update(self) -> None:
        """Fetch the latest balance from SIPNET."""
        session = async_get_clientsession(self.hass)
        params = {"sipuid": self._sipuid, "password": self._password}

        try:
            async with async_timeout.timeout(15):
                async with session.get(API_URL, params=params, ssl=True) as resp:
                    text = await resp.text()

            # Parse XML: <balance value="337.63" ...
            match = re.search(r'balance value=\"([0-9.]+)\"', text)
            if not match:
                # Try without escaped quotes just in case
                match = re.search(r'balance value="([0-9.]+)"', text)

            if match:
                try:
                    self._attr_native_value = float(match.group(1))
                except ValueError:
                    _LOGGER.error(
                        "SIPNET: could not convert '%s' to float", match.group(1)
                    )
                    self._attr_native_value = None
            else:
                _LOGGER.error("SIPNET: could not find balance in response: %s", text)
                self._attr_native_value = None

        except Exception as err:  # noqa: BLE001
            _LOGGER.error("SIPNET: error fetching balance: %s", err)
            self._attr_native_value = None
