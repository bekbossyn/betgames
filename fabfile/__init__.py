from . import common

from fabric.decorators import task
from fabric.state import env

env.repository = "https://github.com/DAKZH/betgames"
env.user = "root"
env.password = "BetMates1"
env.hosts = ["45.55.176.109"]
