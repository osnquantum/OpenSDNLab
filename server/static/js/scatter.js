let scatterChart;


async function loadScatter(exp){


    const response =
    await fetch(
        "/api/analytics/scatter/" + exp
    );


    const result =
    await response.json();



    const points =
    result.data.rtt_throughput.x.map(

        (x,i)=>({

            x:x,

            y:
            result.data.rtt_throughput.y[i]

        })

    );



    if(scatterChart){

        scatterChart.destroy();

    }



    const ctx =
    document.getElementById(
        "scatterChart"
    );



    scatterChart =
    new Chart(

        ctx,

        {


        type:"scatter",


        data:{


            datasets:[{


                label:
                "RTT vs Throughput",


                data:points,


                pointRadius:6


            }]


        },


        options:{


            responsive:true,


            plugins:{


                title:{


                    display:true,


                    text:
                    "RTT and Throughput Relationship"

                }

            },


            scales:{


                x:{


                    title:{


                        display:true,

                        text:
                        "RTT (ms)"

                    }

                },


                y:{


                    title:{


                        display:true,

                        text:
                        "Throughput (Mbps)"

                    }

                }


            }


        }


        }

    );


}
