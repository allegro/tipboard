function updateDataset(data, tileType) {
    let listOfDataset = [];
    let predefinedColor = ['#303F9F', '#8BC34A', '#0288D1', '#E040FB', '#FF5722'];
    let predefinedLabel = ['label1', 'label2', 'label3', 'label4', 'label5'];
    let predefinedSeries = ['serie1', 'serie2', 'serie3', 'serie4', 'serie5'];
    let rcx = 0;
    let keyforData = ('series_list' in data) ? 'series_list' : 'datasets';
    $.each(data[keyforData], function (index, dataset) {
        let tileData = {
            label: ('label' in dataset) ? dataset['label'] : predefinedLabel[rcx++],
            data: ('data' in dataset) ? dataset['data'] : [1, 2, 3, 4, 5],
            fill: (tileType === 'cumulative_flow'),
            backgroundColor: ('backgroundColor' in dataset) ? dataset['backgroundColor'] : predefinedColor[rcx++],
            borderColor: ('backgroundColor' in dataset) ? dataset['backgroundColor'] : predefinedColor[rcx++],
        };
        if (tileType === 'cumulative_flow') {
            tileData['trendlineLinear'] = {
                'lineStyle': 'dotted',
                'width': 2
            }
        } else {
            delete tileData['backgroundColor']
        }
        listOfDataset.push(tileData);
    });
    return {
        labels: ('labels' in data) ? data['labels'] : predefinedSeries,
        datasets: listOfDataset,
        borderColor: ['red', 'green', 'blue']
    };
}

/**
 * This will update the line chart & the cummulative flow
 */
function updateTileLinejs(tileId, data, meta, tileType) {
    console.log("line_chartjs::updateTile::start" + tileId);
    meta['options']['title'] = getTitleForChartJSTitle(data);
    new Chart(document.getElementById(tileId + '-chart'), {
        type: 'line',
        data: updateDataset(data, tileType),
        options: meta['options']
    });
    console.log("linejs::type(" + tileType + ")::updateTile " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('line_chart', updateTileLinejs);

