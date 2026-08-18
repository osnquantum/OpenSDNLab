async function loadHeatmap(exp){


    const response = await fetch(
        "/api/analytics/matrix/" + exp
    );


    const result = await response.json();


    if(result.valid === false){

        document.getElementById(
            "correlationHeatmap"
        ).innerHTML = `
        <div class="card">
            <h3>⚠ Correlation Analysis Unavailable</h3>
            <p>${result.message}</p>
            <p>
            Required samples:
            ${result.required_samples}
            </p>
            <p>
            Available samples:
            ${result.available_samples}
            </p>
        </div>
        `;

        return;
    }


    const matrix = result.matrix;


    const labels = Object.keys(matrix);



    let html = `

    <table style="
    border-collapse:collapse;
    margin-top:20px">

    <tr>
    <th style="padding:15px">
    Metric
    </th>
    `;


    labels.forEach(label=>{

        html += `
        <th style="padding:15px">
        ${label}
        </th>
        `;

    });


    html += "</tr>";



    labels.forEach(row=>{


        html += `

        <tr>

        <th style="padding:15px">
        ${row}
        </th>

        `;



        labels.forEach(col=>{


            let value =
            matrix[row][col];


            let intensity =
            Math.abs(value);



            html += `

            <td style="
            padding:20px;
            text-align:center;
            background:
            rgba(0,100,255,${intensity});
            color:white;
            font-weight:bold">

            ${value.toFixed(3)}

            </td>

            `;


        });


        html += "</tr>";


    });



    html += "</table>";



    document.getElementById(
        "correlationHeatmap"
    ).innerHTML = html;


}
