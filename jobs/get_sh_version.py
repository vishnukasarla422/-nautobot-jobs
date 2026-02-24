from nautobot.apps.jobs import Job

class GetShVersion(Job):
    class Meta:
        name = "Get SH Version"
        description = "Runs sh --version on the container"

    def run(self):
        import subprocess
        result = subprocess.run(["sh", "--version"], capture_output=True, text=True)
        self.logger.info(result.stdout or result.stderr)
```

**3. Push to GitHub**
```
git add get_sh_version.py
git commit -m "Add get sh version job"
git push
