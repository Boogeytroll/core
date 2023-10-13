"""Support for SwitchBot Meter sensors."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType

from . import SwitchbotCloudData
from .const import DOMAIN
from .entity import SwitchBotCloudEntity

async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up SwitchBot Meter sensors."""
    data: SwitchbotCloudData = hass.data[DOMAIN][config.entry_id]
    async_add_entities(
        SwitchBotMeterSensor(data.api, device, coordinator)
        for device, coordinator in data.devices.meters
    )

class SwitchBotMeterSensor(SwitchBotCloudEntity, SensorEntity):
    """Representation of a SwitchBot Meter sensor."""

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def name(self):
        return self._attr_device_info["name"]

    @property
    def state(self):
        """Return the state of the sensor."""
        # Your logic here to determine the state of the sensor
        # This might involve fetching the latest data from the coordinator
        # and returning the relevant attribute as the state.

        # Example:
        # Assuming the coordinator stores the latest data in `self.coordinator.data`
        # and this data includes a `temperature` attribute for temperature meters
        if self._switchbot_state["deviceType"] == "TemperatureMeter":
            return self.coordinator.data.get("temperature")
        elif self._switchbot_state["deviceType"] == "HumidityMeter":
            return self.coordinator.data.get("humidity")
        else:
            return None

    @property
    def unit_of_measurement(self):
        if self._switchbot_state["deviceType"] == "TemperatureMeter":
            return "°C"
        elif self._switchbot_state["deviceType"] == "HumidityMeter":
            return "%"
        else:
            return None

    @property
    def device_class(self):
        """Return the class of the sensor."""
        # Your logic here to determine the device class of the sensor
        # This might involve checking the type of the meter (e.g., temperature, humidity)
        # and returning the appropriate device class.

        # Example:
        if self._switchbot_state["deviceType"] == "TemperatureMeter":
            return "temperature"
        elif self._switchbot_state["deviceType"] == "HumidityMeter":
            return "humidity"
        else:
            return None

    def _handle_coordinator_update(self):
        """Handle updated data from the coordinator."""
        # Your logic here to update the internal state of the entity
        # based on the latest data from the coordinator.

        # Example:
        # Assuming the coordinator stores the latest data in `self.coordinator.data`
        # and this data includes a `temperature` attribute for temperature meters
        if self._switchbot_state["deviceType"] == "TemperatureMeter":
            self._attr_state = self.coordinator.data.get("temperature")
        elif self._switchbot_state["deviceType"] == "HumidityMeter":
            self._attr_state = self.coordinator.data.get("humidity")
        else:
            self._attr_state = None

        # Ensure to call the superclass method to handle any additional update logic
        # and update the entity in Home Assistant.
        super()._handle_coordinator_update()
