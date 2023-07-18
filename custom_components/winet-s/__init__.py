""" Sungrow WiNet-S   by ozziii   """
from __future__ import annotations

import logging


from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN,WINETS_FLOW_IP_STR
from .coordinator import WiNetDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


PLATFORMS = [Platform.SENSOR]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up WiNet-S component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WiNet-S from a config entry."""
    _LOGGER.debug("Setup ID: %s ", entry.entry_id)

    address = entry.data[WINETS_FLOW_IP_STR]

    coordinator = WiNetDataUpdateCoordinator(hass,address)

    try:
        await coordinator.async_init_data()
        hass.data[DOMAIN][entry.entry_id] = coordinator
    except HomeAssistantError as err:
        _LOGGER.error(err)
        return False
        
    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
