"""The Berlin (BVG) and Brandenburg (VBB) transport integration."""
from __future__ import annotations
import logging
from typing import Optional
from datetime import datetime, timedelta

import requests
import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from .const import (  # pylint: disable=unused-import
    DOMAIN,  # noqa
    SCAN_INTERVAL,  # noqa
    API_ENDPOINT,
    CONF_DEPARTURES,
    CONF_DEPARTURES_TRACK,
    CONF_AVV_WIDGET_ID,
    CONF_TYPE_BUS,
    CONF_TYPE_FERRY,
    CONF_TYPE_EXPRESS,
    CONF_TYPE_REGIONAL,
    CONF_TYPE_SUBURBAN,
    CONF_TYPE_SUBWAY,
    CONF_TYPE_TRAM,
    CONF_DEPARTURES_NAME,
    DEFAULT_ICON,
)
from .departure import Departure

_LOGGER = logging.getLogger(__name__)

TRANSPORT_TYPES_SCHEMA = {
    vol.Optional(CONF_TYPE_SUBURBAN, default=True): bool,
    vol.Optional(CONF_TYPE_SUBWAY, default=True): bool,
    vol.Optional(CONF_TYPE_TRAM, default=True): bool,
    vol.Optional(CONF_TYPE_BUS, default=True): bool,
    vol.Optional(CONF_TYPE_FERRY, default=True): bool,
    vol.Optional(CONF_TYPE_EXPRESS, default=True): bool,
    vol.Optional(CONF_TYPE_REGIONAL, default=True): bool,
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_DEPARTURES): [
            {
                vol.Required(CONF_DEPARTURES_NAME): str,
                vol.Required(CONF_AVV_WIDGET_ID): str,
                vol.Optional(CONF_DEPARTURES_TRACK): int,
                **TRANSPORT_TYPES_SCHEMA,
            }
        ]
    }
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    _: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    if CONF_DEPARTURES in config:
        for departure in config[CONF_DEPARTURES]:
            add_entities([TransportSensor(hass, departure)])


class TransportSensor(SensorEntity):
    departures: list[Departure] = []

    def __init__(self, hass: HomeAssistant, config: dict) -> None:
        self.hass: HomeAssistant = hass
        self.config: dict = config
        self.avv_widget_id: str = config[CONF_AVV_WIDGET_ID]
        self.sensor_name: str | None = config.get(CONF_DEPARTURES_NAME)
        self.track: int | None = config.get(CONF_DEPARTURES_TRACK)

    @property
    def name(self) -> str:
        return self.sensor_name or f"Stop ID: {self.avv_widget_id}"

    @property
    def icon(self) -> str:
        next_departure = self.next_departure()
        if next_departure:
            return next_departure.icon
        return DEFAULT_ICON

    @property
    def unique_id(self) -> str:
        return f"stop_{self.avv_widget_id}_{self.sensor_name}_departures"

    @property
    def state(self) -> str:
        next_departure = self.next_departure()
        if next_departure:
            return f"Next {next_departure.line_name} at {next_departure.time}"
        return "N/A"

    @property
    def extra_state_attributes(self):
        return {
            "departures": [departure.to_dict() for departure in self.departures or []]
        }

    def update(self):
        self.departures = self.fetch_departures()

    def fetch_departures(self) -> Optional[list[Departure]]:
        try:
            response = requests.get(
                url=f"{API_ENDPOINT}{self.avv_widget_id}",
                timeout=30,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            _LOGGER.warning(f"API error: {ex}")
            return []
        except requests.exceptions.Timeout as ex:
            _LOGGER.warning(f"API timeout: {ex}")
            return []

        _LOGGER.debug(f"OK: departures for {self.avv_widget_id}: {response.text}")

        # parse JSON response
        try:
            departures: list = list(response.json()["fahrten"].values())[0]["abfahrt"]
        except requests.exceptions.InvalidJSONError as ex:
            _LOGGER.error(f"API invalid JSON: {ex}")
            return []

        # keep departures only from the relevant track
        if self.track:
            for i in list(departures):
                track = i.get("track")
                if str(self.track) not in str(track):  # e.g. '1' not in 'H.1'
                    departures.remove(i)

        # convert api data into objects
        unsorted = [Departure.from_dict(departure) for departure in departures]
        return sorted(unsorted, key=lambda d: d.timestamp)

    def next_departure(self):
        if self.departures and isinstance(self.departures, list):
            return self.departures[0]
        return None
