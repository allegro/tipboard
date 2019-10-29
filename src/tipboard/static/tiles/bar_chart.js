function buildDatasets(data) {
    let listOfDataset = [];
    let predefinedColor = ['#303F9F', '#8BC34A', '#0288D1', '#E040FB', '#FF5722'];
    let rcx = 0;
    if ('series_list' in data) { // Eazy way: no config
        $.each(data['series_list'],function(index, serie) {
            listOfDataset.push({
                label: '',
                data: serie,
                backgroundColor: predefinedColor[rcx++]
            });
        });
    } else { // full conf
        $.each(data['datasets'],function(index, dataset){
            listOfDataset.push({
                label: ('label' in dataset) ? dataset['label'] : '',
                data: ('data' in dataset) ? dataset['data'] : [],
                backgroundColor: ('backgroundColor' in dataset) ? dataset['backgroundColor'] : predefinedColor[rcx++]
            });
        });
    }
    return listOfDataset;
}

function updateBarChartjs(tileId, data, meta, tileType) {
    console.log("bar_chartjs::type(" + tileType +")::updateTile::start" + tileId);
    meta['options']['title'] = getTitleForChartJSTitle(data);
    new Chart(document.getElementById(tileId + '-chart'), {
            type: (tileType === 'vbar_chart') ? 'bar' : 'horizontalBar',
            data: {
                labels: data['labels'],
                datasets: buildDatasets(data),
            },
            options: meta['options']
    });
    console.log("bar_chartjs::type(" + tileType +")::updateTile::end " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('bar_chart', updateBarChartjs);
