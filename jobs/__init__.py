from nautobot.apps.jobs import register_jobs
from .add_router_job import AddRouter

register_jobs(AddRouter)
