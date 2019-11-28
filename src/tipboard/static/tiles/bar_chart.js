// la bart chart affiche une couleur par dataset, dans le EF500 ooc, il y a 4 value but 1 dataset, dc 1 color
// Si tu met 4 dataset et len(data.labels) == 1 alors le backgroundColor fonctione par bar
// le nombre de data.labels définit combien de data seront affiché depuis les datasets
function buildDatasets(data) {
    let listOfDataset = [];
    $.each(data['datasets'],function(index, dataset) {
        let datasetTmp = {
            label: ('label' in dataset) ? dataset['label'] : '',
            data: ('data' in dataset) ? dataset['data'] : [],
            backgroundColor: ('backgroundColor' in dataset) ?
                dataset['backgroundColor'] : Tipboard.Palette.tabColor[index]
        };
        listOfDataset.push(datasetTmp);
    });
    return listOfDataset;
}

function updateBarChartjs(tileId, data, meta, tileType) {
    console.log("bar_chartjs::type(" + tileType + ")::updateTile::start");
    meta['options']['title'] = getTitleForChartJSTitle(data);
    new Chart(document.getElementById(tileId + '-chart'), {
        type: (tileType === 'vbar_chart') ? 'bar' : 'horizontalBar',
        data: {
            labels: data['labels'],
            datasets: buildDatasets(data),
        },
        options: meta['options']
    });
    console.log("bar_chartjs::type(" + tileType + ")::updateTile::end " + tileId);
}

Tipboard.Dashboard.registerUpdateFunction('bar_chart', updateBarChartjs);
