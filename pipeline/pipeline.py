"""
OpenSDNLab Processing Pipeline
"""


class Pipeline:

    def __init__(self):

        self.steps = []

    ############################################################

    def add_step(

        self,

        name,

        function

    ):

        self.steps.append(

            (

                name,

                function

            )

        )

    ############################################################

    def execute(

        self,

        data

    ):

        current = data

        for name, function in self.steps:

            print()

            print("=" * 60)

            print("Pipeline Step:", name)

            current = function(current)

        return current
