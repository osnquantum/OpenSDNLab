from controllers.controller_manager import ControllerManager

manager = ControllerManager()

############################################################

local = manager.create({

    "type": "local"

})

print(local.name())

############################################################

ryu = manager.create({

    "type": "remote",

    "name": "ryu",

    "ip": "127.0.0.1",

    "port": 6653

})

print(ryu.name())

############################################################

onos = manager.create({

    "type": "remote",

    "name": "onos",

    "ip": "192.168.1.10",

    "port": 6653

})

print(onos.name())

############################################################

floodlight = manager.create({

    "type": "remote",

    "name": "floodlight",

    "ip": "192.168.1.20",

    "port": 6653

})

print(floodlight.name())

