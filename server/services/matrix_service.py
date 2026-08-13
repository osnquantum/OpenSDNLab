import statistics


class MatrixService:


    def pearson(self,x,y):

        x=[float(v) for v in x]
        y=[float(v) for v in y]


        if len(x) < 2 or len(y) < 2:
            return 0


        n=min(len(x),len(y))

        x=x[:n]
        y=y[:n]


        mx=statistics.mean(x)
        my=statistics.mean(y)


        num=sum(
            (a-mx)*(b-my)
            for a,b in zip(x,y)
        )


        den=(

            sum((a-mx)**2 for a in x)
            *
            sum((b-my)**2 for b in y)

        )**0.5


        if den==0:
            return 0


        return round(num/den,4)



    def calculate(self,data):


        metrics={

            "RTT":data["rtt"],

            "Jitter":data["jitter"],

            "Throughput":data["throughput"],

            "Delay":data["one_way_delay"]

        }


        matrix={}


        for a in metrics:

            matrix[a]={}

            for b in metrics:

                matrix[a][b]=self.pearson(
                    metrics[a],
                    metrics[b]
                )


        return matrix
