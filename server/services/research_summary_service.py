class ResearchSummaryService:


    def effect_interpretation(self, d):

        d = abs(d)

        if d < 0.2:
            return "Negligible"

        elif d < 0.5:
            return "Small"

        elif d < 0.8:
            return "Medium"

        else:
            return "Large"



    def generate(self, comparison, statistics):


        rtt = comparison["rtt"]


        if statistics["significant"]:

            significance = (
                "Statistically significant "
                "difference detected"
            )

        else:

            significance = (
                "No statistically significant "
                "difference detected"
            )



        if rtt["difference"] < 0:

            latency_result = (
                "Experiment B has lower latency"
            )

        else:

            latency_result = (
                "Experiment A has lower latency"
            )



        return {


            "performance_summary": {

                "latency":
                latency_result,

                "rtt_difference":
                rtt["difference"],

                "rtt_improvement_percent":
                rtt["improvement"]

            },


            "statistical_summary": {

                "p_value":
                statistics["p_value"],

                "cohens_d":
                statistics["cohens_d"],

                "effect":
                self.effect_interpretation(
                    statistics["cohens_d"]
                ),

                "decision":
                significance

            },


            "research_conclusion":

            latency_result
            + ". "
            + significance
            + "."

        }
