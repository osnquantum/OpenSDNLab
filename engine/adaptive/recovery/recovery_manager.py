"""
Adaptive Recovery Manager

Coordinates recovery strategies.
"""


class RecoveryManager:


    def __init__(self):

        self.strategies = {}


    def register(
        self,
        name,
        strategy
    ):

        self.strategies[name] = strategy


    def execute(
        self,
        strategy_name,
        network,
        controller,
        metrics,
        trigger,
        inventory=None
    ):

        strategy = self.strategies.get(
            strategy_name
        )

        if strategy is None:

            return {

                "executed": False,

                "success": False,

                "strategy": strategy_name,

                "reason":
                    "Recovery strategy not available"

            }


        try:

            result = strategy.execute(

                network=network,

                controller=controller,

                metrics=metrics,

                trigger=trigger,

                inventory=inventory

            )


            result.setdefault(
                "executed",
                True
            )

            result.setdefault(
                "strategy",
                strategy_name
            )

            return result


        except Exception as error:

            return {

                "executed": True,

                "success": False,

                "strategy": strategy_name,

                "error": str(error)

            }


recovery_manager = RecoveryManager()
