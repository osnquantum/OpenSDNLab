let dataset = null;


const metricInfo = {

    rtt:{
        name:"Round Trip Time",
        unit:"ms"
    },

    throughput:{
        name:"Throughput",
        unit:"Mbps"
    },

    jitter:{
        name:"Jitter",
        unit:"ms"
    },

    one_way_delay:{
        name:"One Way Delay",
        unit:"ms"
    },

    packet_loss:{
        name:"Packet Loss",
        unit:"%"
    },

    mos:{
        name:"Mean Opinion Score",
        unit:"MOS"
    }

};



async function loadAnalytics(exp, jobId=null){


    let url =
        "/api/analytics/data/" +
        encodeURIComponent(exp);


    if(jobId){

        url +=
            "?job_id=" +
            encodeURIComponent(jobId);

    }


    console.log(
        "Loading analytics:",
        {
            experiment_id: exp,
            job_id: jobId,
            url: url
        }
    );


    let response =
        await fetch(url);


    dataset =
        await response.json();


    if(!dataset.success){

        console.error(
            "Analytics loading failed:",
            dataset
        );

        return;

    }


    createChart();

}





function getSelectedMetrics(){


    return Array.from(

        document.querySelectorAll(
            ".metricBox:checked"
        )

    ).map(

        item => item.value

    );

}





function createChart(){


    let metrics =
    getSelectedMetrics();



    if(metrics.length===0)
        return;



    let chartType =
    document.getElementById(
        "chartType"
    ).value;




    let datasets = metrics.map(

        metric => ({

            label:
            metricInfo[metric].name
            +
            " ("
            +
            metricInfo[metric].unit
            +
            ")",


            data:
            dataset.data[metric],


            borderWidth:2,

            tension:0.3

        })

    );




    if(window.myChart){

        window.myChart.destroy();

    }



    let ctx =
    document.getElementById(
        "researchChart"
    );



    window.myChart =
    new Chart(

        ctx,

        {


        type:chartType,


        data:{


            labels:
            dataset.data.runs,


            datasets:datasets


        },


        options:{


            responsive:true,


            plugins:{


                title:{


                    display:true,


                    text:
                    "OpenSDN Research Metric Analysis"


                }


            },


            scales:{


                x:{


                    title:{


                        display:true,

                        text:"Experiment Run"

                    }

                },


                y:{


                    title:{


                        display:true,

                        text:"Measured Value"

                    },


                    beginAtZero:true


                }


            }


        }


        }

    );


}
