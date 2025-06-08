from .cpu import cpu
from .mem import mem
from .disk import disk
from .net import net
from .uptime import uptime
from .proc import proc
from .help import help
from .who import who
from .env import env
from .top import top
from .ports import ports
from .crontab import crontab


def register_commands(interpreter):
    interpreter.commands["cpu"] = cpu
    interpreter.commands["mem"] = mem
    interpreter.commands["disk"] = disk
    interpreter.commands["net"] = net
    interpreter.commands["uptime"] = uptime
    interpreter.commands["proc"] = proc
    interpreter.commands["help"] = help
    interpreter.commands["who"] = who
    interpreter.commands["env"] = env
    interpreter.commands["top"] = top
    interpreter.commands["ports"] = ports
    interpreter.commands["crontab"] = crontab
