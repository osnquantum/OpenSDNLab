from core.configuration import config

print()

print("Application Name : ", config.get("application.name"))

print("Version          : ", config.get("application.version"))

print("Protocol         : ", config.get("network.protocol"))

print("Database         : ", config.get("database.path"))

print()

config.set("network.protocol", "dual")

config.save()

print("Updated protocol:", config.get("network.protocol"))
