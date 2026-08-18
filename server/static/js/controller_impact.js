let controllerImpactChart = null;


async function loadControllerImpact(exp){

    const response = await fetch(
        "/api/analytics/controller-impact/" + exp
    );

    const data = await response.json();


    if(!data.success){
        console.log(data.message);
        return;
    }


    const analysis = data.analysis;


    const ctx = document.getElementById(
        "controllerImpactChart"
    );


    if(controllerImpactChart){
        controllerImpactChart.destroy();
    }


    controllerImpactChart = new Chart(
        ctx,
        {
            type:"bar",

            data:{
                labels:[
                    "Packet-In vs RTT",
                    "Flow Install vs RTT",
                    "Memory vs RTT"
                ],

                datasets:[
                    {
                        label:"Correlation",

                        data:[
                            analysis.packet_in_vs_rtt,
                            analysis.flow_install_vs_rtt,
                            analysis.memory_vs_rtt
                        ]
                    }
                ]
            },

            options:{
                responsive:true,

                scales:{
                    y:{
                        beginAtZero:true,
                        max:1,
                        min:-1
                    }
                }
            }
        }
    );

}
