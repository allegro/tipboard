function updateTilePiejs(tileId, data, meta, tileType) {
    var ctx = document.getElementById(tileId + '-chart');
    let isTitle = true;
    if (data['title'] === 'undefined') {
        isTitle = false;
        data['title'] = '';
    }

    let tileTitle = {
        display: isTitle,
        text: data['title']
    };
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data['pie_data_tag'],
            datasets: [{
                label: data['label'],
                backgroundColor: meta['backgroundColor'],
                data: data['pie_data_value'],
                borderColor: data['borderColor'],
                borderWidth: data['borderWidth'],
            }]
        },
        options: {
            responsive: true,
            legend: {
                display: true,
                position: 'top',
            },
            title: tileTitle,
            maintainAspectRatio: false,
            tooltips: {
                enabled: false
            },
            plugins: {
                labels: {
                    fontColor: 'rgba(255, 255, 255, 0.80)',
                },
                datalabels: {
                    formatter: (value, ctx) => {
                        let sum = 0;
                        let dataArr = ctx.chart.data.datasets[0].data;
                        dataArr.map(data => {
                            sum += data;
                        });
                        return (value * 100 / sum).toFixed(2) + "%";
                    },
                }
            },
        }
    });
}

Tipboard.Dashboard.registerUpdateFunction('pie_chart', updateTilePiejs);
