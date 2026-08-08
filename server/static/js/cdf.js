let cdfChart;


async function loadCDF(exp){


    const response =
    await fetch(
        "/api/analytics/cdf/" + exp
    );


    const result =
    await response.json();



    const points =
    result.cdf;



    if(cdfChart){

        cdfChart.destroy();

    }



    const ctx =
    document.getElementById(
        "cdfChart"
    );



    cdfChart =
    new Chart(

        ctx,

        {


        type:"line",


        data:{


            datasets:[{

                label:
                "RTT CDF",


                data:points,


                parsing:false,


                borderWidth:3,


                pointRadius:5


            }]


        },


        options:{


            responsive:true,


            plugins:{


                title:{


                    display:true,

                    text:
                    "RTT Cumulative Distribution Function"

                }


            },


            scales:{


                x:{


                    type:"linear",


                    title:{


                        display:true,

                        text:
                        "RTT (ms)"

                    }

                },


                y:{


                    min:0,

                    max:1,


                    title:{


                        display:true,

                        text:
                        "CDF Probability"

                    }

                }


            }


        }


        }

    );


}
