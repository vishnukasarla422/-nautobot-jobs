from nautobot.apps.jobs import Job, StringVar, ObjectVar
from nautobot.dcim.models import Device, DeviceType, Location
from nautobot.extras.models import Role, Status


class AddRouter(Job):
    class Meta:
        name = "Add Router"
        description = "Add a new router device to Nautobot"

    device_name = StringVar(
        description="Name of the router (e.g. R2, R3)",
        label="Device Name",
    )
    location = ObjectVar(
        model=Location,
        description="Location to place the device",
        label="Location",
    )
    device_type = ObjectVar(
        model=DeviceType,
        description="Device type (e.g. c7200)",
        label="Device Type",
    )

    def run(self, device_name, location, device_type):
        try:
            role = Role.objects.get(name="Router")
        except Role.DoesNotExist:
            self.logger.error("Role 'Router' not found.")
            return
        status = Status.objects.get(name="Active")
        if Device.objects.filter(name=device_name).exists():
            self.logger.warning(f"Device '{device_name}' already exists!")
            return
        device = Device(
            name=device_name,
            device_type=device_type,
            role=role,
            location=location,
            status=status,
        )
        device.validated_save()
        self.logger.info(f"Router '{device_name}' created!", extra={"object": device})
