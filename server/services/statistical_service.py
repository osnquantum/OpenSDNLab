import statistics
import math

from scipy import stats



class StatisticalService:


    def cohens_d(self,a,b):

        mean_diff = statistics.mean(a)-statistics.mean(b)

        pooled = math.sqrt(
            (
                statistics.variance(a)
                +
                statistics.variance(b)
            )/2
        )

        if pooled == 0:
            return 0

        return round(
            mean_diff/pooled,
            3
        )



    def analyze(self,a,b):


        if len(a) < 2 or len(b) < 2:

            return {

                "status":"NO_DATA",

                "message":"Insufficient samples",

                "mean_a":0,

                "mean_b":0,

                "difference":0,

                "std_a":0,

                "std_b":0,

                "cohens_d":0,

                "p_value":1,

                "significant":False

            }


        t_stat,p_value = stats.ttest_ind(
            a,
            b,
            equal_var=False
        )


        return {


            "mean_a":
            round(statistics.mean(a),3),


            "mean_b":
            round(statistics.mean(b),3),


            "difference":
            round(
                statistics.mean(b)
                -
                statistics.mean(a),
                3
            ),


            "std_a":
            round(
                statistics.stdev(a),
                3
            )
            if len(a)>1 else 0,


            "std_b":
            round(
                statistics.stdev(b),
                3
            )
            if len(b)>1 else 0,


            "cohens_d":
            self.cohens_d(a,b),


            "p_value":
            round(
                p_value,
                5
            ),


            "significant":
            bool(p_value < 0.05)

        }
