// la bart chart affiche une couleur par dataset, dans le EF500 ooc, il y a 4 value but 1 dataset, dc 1 color
// Si tu met 4 dataset et len(data.labels) == 1 alors le backgroundColor fonctione par bar
// le nombre de data.labels définit combien de data seront affiché depuis les datasets

// aujourd'hui tu as considéré que les couleurs par défaut venait du redis, set par le FakeDataObject
// ce qui empeche d'avoir les couleurs de maniere générique dans palette.js
// donc soit le generic est dans le .js, soit dans django

// si on gere ca dans python, il faut config la meta des tiles à chaque push parfaitement
// MetaConfig.py pour chaque tiles ?
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

function buildMeta(meta) {
    return {
                'scale': {
                    'gridLines': {
                        'color': ['#525252', '#525252', '#525252', '#525252', '#525252', '#525252', '#525252']
                    },
                    'angleLines': {'color': '#525252'},
                    'ticks': {'display': false}
                },
                'responsive': true,
                'maintainAspectRatio': false,
            };
    // if (meta['options']['backgroundColor']) {
    //
    // }
    // return meta['options'];
}

function updateBarChartjs(tileId, data, meta, tileType) {
    let chart = document.getElementById(tileId + '-chart');
   // meta['options']['title'] = getTitleForChartJSTitle(data);
    new Chart(chart, {
        type: (tileType === 'vbar_chart') ? 'bar' : 'horizontalBar',
        data: {
            labels: data['labels'],
            datasets: buildDatasets(data),
        },
        options: buildMeta(meta)
    });
}

Tipboard.Dashboard.registerUpdateFunction('bar_chart', updateBarChartjs);
