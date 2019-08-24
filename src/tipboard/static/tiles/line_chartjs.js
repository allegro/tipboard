
function updateTileLinejs(tileId, data, meta, tipboard) {
    console.log("line_chartjs::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['last(n)', 'n-1', 'n-2',],
                datasets: [{
                    label: '# Velocity of squad',
                    data: [12, 19, 3],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
    });

    // update setDataByKeys => 'subtitle', 'description'
    // config creation
    // renderersSwapper.swap(meta);
    // init graph color
    // update actual data of tile
    console.log("line_chartjs::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('line_chartjs', updateTileLinejs);

