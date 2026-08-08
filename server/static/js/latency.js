let latencyChart;


async function loadLatency(exp){


    const response =
    await fetch(
        "/api/analytics/latency/" + exp
    );


    const result =
    await response.json();



    const cdf =
    result.cdf;



    if(latencyChart){

        latencyChart.destroy();

    }



    const ctx =
    document.getElementById(
        "latencyChart"
    );



    latencyChart =
    new Chart(

        ctx,

        {


        type:"line",


        data:{


            datasets:[{

                label:
                "RTT CDF",


                data:cdf,


                parsing:false,


                borderWidth:3,


                pointRadius:5

            }]


        },


        options:{


            responsive:true,


            scales:{


                x:{

                    type:"linear",

                    title:{

                        display:true,

                        text:"RTT (ms)"

                    }

                },


                y:{

                    min:0,

                    max:1,

                    title:{

                        display:true,

                        text:"Probability"

                    }

                }


            },


            plugins:{


                title:{


                    display:true,

                    text:
                    "Latency Distribution (CDF)"

                }


            }


        }

        }

    );



    document.getElementById(
        "p50"
    ).innerHTML =
    result.percentile.P50+" ms";


    document.getElementById(
        "p90"
    ).innerHTML =
    result.percentile.P90+" ms";


    document.getElementById(
        "p95"
    ).innerHTML =
    result.percentile.P95+" ms";


    document.getElementById(
        "p99"
    ).innerHTML =
    result.percentile.P99+" ms";


    document.getElementById(
        "meanRTT"
    ).innerHTML =
    result.statistics.mean+" ms";


    document.getElementById(
        "medianRTT"
    ).innerHTML =
    result.statistics.median+" ms";


}
