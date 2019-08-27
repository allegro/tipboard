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
        options: meta['options']
    });
    console.log("pie_chartjs::updateTile end" + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('pie_chartjs', updateTilePiejs);
