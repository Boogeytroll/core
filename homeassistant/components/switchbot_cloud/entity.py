class SwitchBotCloudEntity(CoordinatorEntity[SwitchBotCoordinator]):
    """Representation of a SwitchBot Cloud entity."""

    _api: SwitchBotAPI
    _switchbot_state: dict[str, Any] | None = None
    _attr_has_entity_name = True

    def __init__(
        self,
        api: SwitchBotAPI,
        device: Device | Remote,
        coordinator: SwitchBotCoordinator,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._api = api
        self._attr_unique_id = device.device_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device.device_id)},
            name=device.device_name,
            manufacturer="SwitchBot",
            model=device.device_type,
        )

    async def send_command(
        self,
        command: Commands,
        command_type: str = "command",
        parameters: dict | str = "default",
    ) -> None:
        """Send command to device."""
        await self._api.send_command(
            self._attr_unique_id,
            command,
            command_type,
            parameters,
        )

    @property
    def current_value(self) -> float | None:
        """Return the current value of the meter."""
        # Your logic here to determine the current value of the meter
        # This might involve fetching the latest data from the coordinator
        # and returning the relevant attribute as the current value.

        # Example:
        # Assuming the coordinator stores the latest data in `self.coordinator.data`
        # and this data includes a `value` attribute for meter devices
        return self.coordinator.data.get("value")
