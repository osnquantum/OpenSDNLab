import statistics


class LatencyService:


    def percentile(self, values, p):

        values = sorted(values)

        if not values:
            return 0


        index = (len(values)-1)*p

        low=int(index)

        high=min(
            low+1,
            len(values)-1
        )

        weight=index-low


        return round(
            values[low] +
            weight*(values[high]-values[low]),
            3
        )



    def analyze(self, values):

        values=sorted(values)


        cdf=[]

        total=len(values)


        for i,v in enumerate(values):

            cdf.append({

                "x":v,

                "y":round(
                    (i+1)/total,
                    4
                )

            })


        return {


            "cdf":cdf,


            "percentile":{

                "P50":
                self.percentile(values,0.50),

                "P90":
                self.percentile(values,0.90),

                "P95":
                self.percentile(values,0.95),

                "P99":
                self.percentile(values,0.99)

            },


            "statistics":{

                "mean":
                round(
                    statistics.mean(values),
                    3
                ),

                "median":
                round(
                    statistics.median(values),
                    3
                ),

                "min":
                min(values),

                "max":
                max(values)

            }

        }
