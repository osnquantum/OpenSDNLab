from engine.adaptive.recovery.recovery_manager import recovery_manager
from engine.adaptive.recovery.path_recovery import PathRecovery

recovery_manager.register(
    "PATH_RECOVERY",
    PathRecovery()
)
