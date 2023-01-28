"""The Aachen (AVV) transport integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, SCAN_INTERVAL  # noqa


def setup(hass: HomeAssistant, config: ConfigType) -> bool:  # pylint: disable=unused-argument
    return True
