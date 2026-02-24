from nautobot.core.celery import register_jobs
from nautobot.apps.jobs import Job
import subprocess

class GetShVersion(Job):
    class Meta:
        name = "Get SH Version"
        description = "Runs sh --version on the container"

    def run(self):
        result = subprocess.run(["sh", "--version"], capture_output=True, text=True)
        self.logger.info(result.stdout or result.stderr)

register_jobs(GetShVersion)
