import statistics


class ComparisonService:


    def improvement(self,a,b,lower=True):

        if a==0:
            return 0

        if lower:
            value=(a-b)/a*100
        else:
            value=(b-a)/a*100

        return round(value,2)



    def summarize(self,a,b):


        if (
            not a.get("rtt") or
            not b.get("rtt") or
            not a.get("throughput") or
            not b.get("throughput")
        ):

            return {

                "status":"NO_DATA",

                "message":"Insufficient experiment data"

            }


        result={}


        result["rtt"]={

            "experiment_a":
            round(statistics.mean(a["rtt"]),3),

            "experiment_b":
            round(statistics.mean(b["rtt"]),3),

            "difference":
            round(
                statistics.mean(b["rtt"]) -
                statistics.mean(a["rtt"]),
                3
            ),

            "improvement":
            self.improvement(
                statistics.mean(a["rtt"]),
                statistics.mean(b["rtt"]),
                True
            )

        }


        result["throughput"]={

            "experiment_a":
            round(statistics.mean(a["throughput"]),3),

            "experiment_b":
            round(statistics.mean(b["throughput"]),3),

            "difference":
            round(
                statistics.mean(b["throughput"]) -
                statistics.mean(a["throughput"]),
                3
            ),

            "improvement":
            self.improvement(
                statistics.mean(a["throughput"]),
                statistics.mean(b["throughput"]),
                False
            )

        }


        return result
