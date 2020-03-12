import random
from src.tipboard.app.properties import COLOR_TAB

# Datasets is always an arrays with the always the same possible value for different chart
# Every dataset is a dict, go to chartJS documentation to see the possibility
# "datasets": [
#       {
#         "label": "Series 1",
#         "fill": true,
#         "data": [ 25, 20 ],
#         "backgroundColor": "rgba(66, 165, 245, 0.8)",
#         "borderColor": "rgba(66, 165, 245, 0.8)",
#         "pointBorderColor": "rgba(66, 165, 245, 0.8)",
#         "pointBackgroundColor": "rgba(255, 255, 255, 0.5)"
#       },
#     ]


def getRandomData(minLenght=0, maxLenght=100, labelLenght=1):
    return [random.randrange(minLenght, maxLenght) for _ in range(1, labelLenght + 1)]


def buildDatasetLine(index=0, randomData=False, labelLenght=24):
    exempleData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    return dict(data=exempleData if randomData is False else getRandomData(1, 30, labelLenght),
                label=f'Line {index + 1}',
                backgroundColor=COLOR_TAB[index],
                fill=False,
                borderColor=COLOR_TAB[index])


def buildDatasetCumulFlow(index=0, randomData=False, labelLenght=9):
    return dict(data=[0, 4, 0, 0, 1, 0, 0, 3, 0, 0] if randomData is False else getRandomData(1, 20, labelLenght),
                label=f'Cumul {index + 1}',
                borderColor=COLOR_TAB[index],
                backgroundColor=COLOR_TAB[index],
                fill=True)


def buildDatasetNorm(index=0, randomData=False, labelLenght=5):
    return dict(data=[2, 20, 13, 33, 85, 100] if randomData is False else getRandomData(2, 100, labelLenght),
                label=f'Series {index + 1}',
                fill=False,
                backgroundColor=COLOR_TAB[index],
                borderColor=COLOR_TAB[index])


def buildDatasetBar(index=0, randomData=False, labelLenght=3):
    return dict(data=[49, 50, 35] if randomData is False else getRandomData(5, 30, labelLenght),
                label=f'Series {index + 1}', backgroundColor=COLOR_TAB[index])


def buildDatasetPolararea(index=0, randomData=False, labelLenght=5):
    return dict(label=f'Section {index}', backgroundColor=COLOR_TAB, borderColor=COLOR_TAB,
                data=[10, 29, 40] if randomData is False else getRandomData(100, 1000, labelLenght))


def buildDatasetPie(index=0, randomData=False, labelLenght=3):
    return dict(label=f'Section {index}', borderColor='#626262', backgroundColor=COLOR_TAB,
                data=[10, 29, 40] if randomData is False else getRandomData(100, 1000, labelLenght), borderWidth=1)


def buildDatasetDoughnut(index=0, randomData=False, labelLenght=4):
    return dict(backgroundColor=COLOR_TAB, borderColor="#626262",
                data=[895, 1478, 1267, 895, 734, 1056, 895, 1056] if randomData is False
                else getRandomData(100, 150, labelLenght),
                label=f'Doughnut {index + 1}')


def buildDatasetRadar(index=0, randomData=False, labelLenght=5):
    return dict(label=f'Series {index + 1}', fill=True,
                data=[18, 10, 36, 36, 40] if randomData is False else getRandomData(4, 50, labelLenght),
                backgroundColor=COLOR_TAB[index], pointBackgroundColor='rgba(255, 255, 255, 0.5)',
                pointBorderColor=COLOR_TAB[index], borderColor=COLOR_TAB[index])


def buildDatasetLinearGauge(index=0, randomData=False, labelLenght=1):
    return dict(label=f'Series {index + 1}', fill=True,
                data=42 if randomData is False else getRandomData(100, 500, labelLenght),
                backgroundColor=COLOR_TAB[index], borderColor='#626262', borderWidth=1,
                pointBorderColor=COLOR_TAB[index], pointBackgroundColor='rgba(255, 255, 255, 0.5)')


def buildGenericDataset(tile_template):
    return dict(pie_chart=buildDatasetPie,
                line_chart=buildDatasetLine,
                cumulative_flow=buildDatasetCumulFlow,
                bar_chart=buildDatasetBar,
                norm_chart=buildDatasetNorm,
                doughnut_chart=buildDatasetDoughnut,
                half_doughnut_chart=buildDatasetDoughnut,
                radar_chart=buildDatasetRadar,
                polararea_chart=buildDatasetPolararea,
                linear_gauge_chart=buildDatasetLinearGauge,
                vbar_chart=buildDatasetBar)[tile_template](index=0, randomData=True, labelLenght=5)
