
function updateTileLinejs(tileId, data, meta, tipboard) {
    console.log("line_chartjs::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
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
    //    var tile = Tipboard.Dashboard.id2node(tileId);

    // update setDataByKeys => 'subtitle', 'description'
    // config creation
    // renderersSwapper.swap(meta);
    // init graph color
    // update actual data of tile
    console.log("line_chartjs::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('line_chartjs', updateTileLinejs);

