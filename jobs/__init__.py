from nautobot.apps.jobs import Job, register_jobs


class AddRouter(Job):
    class Meta:
        name = "Add Router"
        description = "Add a new router device to Nautobot"

    def run(self):
        self.logger.info("Hello from AddRouter!")


register_jobs(AddRouter)
