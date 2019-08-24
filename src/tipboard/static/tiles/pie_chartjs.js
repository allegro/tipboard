
    // update setDataByKeys => 'subtitle', 'description'
    // config creation
    // renderersSwapper.swap(meta);
    // init graph color
    // update actual data of tile
function updateTilePiejs(tileId, data, meta, tipboard) {
    console.log("pie_chartjs::updateTile::start" + tileId);
    var ctx = $('#' + tileId + "-chart");
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ["Pie1", "Pie2", "Pie3",],
            datasets: [{
                label: "Population (millions)",
                backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f",],
                data: [50, 25, 25]
            }]
        },
        options: {
            title: {
                display: true,
                text: 'My Title'
            }
        }
    });
    console.log("pie_chartjs::updateTile" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('pie_chartjs', updateTilePiejs);

