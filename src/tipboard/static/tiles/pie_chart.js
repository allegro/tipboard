/**
 * To see % inside the pie
 */
function buildPlugin(meta) {
    meta.datalabels = {
        formatter: (value, ctx) => {
            let sum = 0;
            let dataArr = ctx.chart.data.datasets[0].data;
            dataArr.map(data => {
                sum += data;
            });
            return (value * 100 / sum).toFixed(2) + "%";
        }
    };
    return meta;
}


function updateTilePiejs(tileId, data, meta, tileType) {
    let chartId = `${tileId}-chart`;
    if (tileId + '-chart' in Tipboard.chartJsTile) {
        Tipboard.Dashboard.updateDataOfChartJS(Tipboard.chartJsTile[chartId], data, meta);
    } else {
        let chartElement = document.getElementById(tileId + "-chart");
        chartElement.parentElement.style.paddingBottom = "10%";
        Tipboard.chartJsTile[tileId + '-chart'] = new Chart(chartElement, {
            type: "pie",
            data: {
                labels: data.labels,
                datasets: data.datasets
            },
            options: buildPlugin(meta)
        });
    }
    console.log("piechart::type(" + tileType + ")::updateTile end " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction("pie_chart", updateTilePiejs);
