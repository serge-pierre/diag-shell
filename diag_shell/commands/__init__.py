from .cpu import cpu
from .mem import mem
from .disk import disk
from .net import net
from .uptime import uptime
from .proc import proc
from .help import help


def register_commands(interpreter):
    interpreter.commands["cpu"] = cpu
    interpreter.commands["mem"] = mem
    interpreter.commands["disk"] = disk
    interpreter.commands["net"] = net
    interpreter.commands["uptime"] = uptime
    interpreter.commands["proc"] = proc
    interpreter.commands["help"] = help
