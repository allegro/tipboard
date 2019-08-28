function updateTilePiejs(tileId, data, meta, tipboard) {
    console.log("pie_chartjs::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    console.log(data);
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data['pie_data_tag'],
            datasets: [{
                label: data['label'],
                backgroundColor: meta['backgroundColor'],
                data: data['pie_data_value']
            }]
        },
        options: {
            tooltips: {
                enabled: false
            },
            plugins: {
                labels: {
                    fontColor: '#fff',
                },
                datalabels: {
                    formatter: (value, ctx) => {
                        let sum = 0;
                        console.log('I format');
                        let dataArr = ctx.chart.data.datasets[0].data;
                        dataArr.map(data => {
                            sum += data;
                        });
                        let percentage = (value * 100 / sum).toFixed(2) + "%";
                        return percentage;
                    },
                }
            },
        }
    });
    console.log("pie_chartjs::updateTile end" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('pie_chartjs', updateTilePiejs);
