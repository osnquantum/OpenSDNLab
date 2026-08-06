from deployment.backends.mininet_backend import MininetBackend

backend = MininetBackend()

backend.initialize()

print()

print("Backend Status")

print("----------------")

print(backend.status())

backend.stop()

print()

print("Backend stopped.")
