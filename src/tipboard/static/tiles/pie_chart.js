/**
 * To see % inside the pie
 */
function buildPlugin() {
    return {
        labels: {
            fontColor: "rgba(255, 255, 255, 0.80)",
        },
        datalabels: {
            formatter: (value, ctx) => {
                let sum = 0;
                let dataArr = ctx.chart.data.datasets[0].data;
                dataArr.map(data => { sum += data; });
                return (value * 100 / sum).toFixed(2) + "%";
            },
        }
    };
}

function buildOption(data) {
    let title = {
        "display": false,
        "text": ""
    };
    if ("title" in data) {
        title["display"] = true;
        title["text"] = data["title"]
    }
    return {
        responsive: true,
        legend: {
            display: true,
            position: "top",
        },
        title: title,
        maintainAspectRatio: false,
        tooltips: {
            enabled: false
        },
        plugins: buildPlugin(),
    }
}

function updateTilePiejs(tileId, data, meta, tileType) {
    let chart = document.getElementById(tileId + "-chart");
    chart.parentElement.style.paddingBottom = "10%";
    new Chart(chart, {
        type: "pie",
        data: {
            labels: data["pie_data_tag"],
            datasets: [{
                label: data["label"],
                backgroundColor: meta["backgroundColor"],
                data: data["pie_data_value"],
                borderColor: data["borderColor"],
                borderWidth: data["borderWidth"],
            }]
        },
        options: buildOption(data)
    });
}

Tipboard.Dashboard.registerUpdateFunction("pie_chart", updateTilePiejs);
