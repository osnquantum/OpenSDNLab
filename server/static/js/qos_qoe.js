async function loadQoSQoEHistory(experiment){

    let response = await fetch(
        "/api/qos-qoe/decisions/" + experiment
    );

    let decisions = await response.json();


    let container = document.getElementById(
        "qosQoeHistory"
    );


    if(!container)
        return;


    if(decisions.length === 0){

        container.innerHTML =
        "<p>No QoS-QoE decisions available</p>";

        return;
    }



    let html = "";


    decisions.forEach(d => {

        let icon =
        d.action === "NO_CHANGE"
        ? "🟢"
        : "🟠";


        html += `
        <div class="qos-item">

            <div class="qos-run">
            Run ${d.run}
            </div>

            <div>
            ${icon} ${d.action}
            </div>

            <div>
            ${d.reason}
            </div>

            <div class="qos-time">
            ${d.time}
            </div>

        </div>
        `;

    });


    container.innerHTML = html;

}
