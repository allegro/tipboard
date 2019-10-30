function buildDatasets(data) {
    let listOfDataset = [];
    let predefinedColor = ['#303F9F', '#8BC34A', '#0288D1', '#E040FB', '#FF5722'];
    let rcx = 0;
    $.each(data['datasets'],function(index, dataset) {
        let datasetTmp = {
            label: ('label' in dataset) ? dataset['label'] : '',
            data: ('data' in dataset) ? dataset['data'] : [],
            backgroundColor: ('backgroundColor' in dataset) ? dataset['backgroundColor'] : predefinedColor[rcx++]
        };
        console.log("new dataset:", datasetTmp);

        listOfDataset.push(datasetTmp);
    });
    return listOfDataset;
}

function updateBarChartjs(tileId, data, meta, tileType) {
    console.log("bar_chartjs::type(" + tileType +")::updateTile::start");
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
