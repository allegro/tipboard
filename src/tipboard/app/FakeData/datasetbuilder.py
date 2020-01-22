import random
from src.tipboard.app.properties import COLOR_TAB


def buildDatasetLine(index=0, randomData=False, labelLenght=24):
    exempleData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    return dict(data=exempleData if randomData is False else [random.randrange(1, 30) for _ in range(labelLenght)],
                label=f'Series {index + 1}',
                borderColor=COLOR_TAB[index], backgroundColor=COLOR_TAB[index], fill=False)


def buildDatasetCumulFlow(index=0, randomData=False, labelLenght=9):
    exempleData = [0, 4, 0, 0, 1, 0, 0, 3, 0, 0]
    return dict(data=exempleData if randomData is False else [random.randrange(1, 20) for _ in range(labelLenght)],
                label=f'Series {index + 1}',
                borderColor=COLOR_TAB[index], backgroundColor=COLOR_TAB[index], fill=True)


def buildDatasetNorm(index=0, randomData=False, labelLenght=5):
    exempleData = [2, 20, 13, 33, 85, 100]
    return dict(data=exempleData if randomData is False else [random.randrange(2, 100) for _ in range(labelLenght)],
                label=f'Series {index + 1}',
                borderColor=COLOR_TAB[index], backgroundColor=COLOR_TAB[index], fill=False)


def buildDatasetBar(index=0, randomData=False, labelLenght=3):
    exempleData = [49, 50, 35]
    return dict(data=exempleData if randomData is False else [random.randrange(5, 30) for _ in range(labelLenght)],
                label=f'Series {index + 1}', backgroundColor=COLOR_TAB[index])


def buildDatasetPolararea(index=0, randomData=False, labelLenght=5):
    data = [random.randrange(100, 1000) for _ in range(1, labelLenght)]
    return dict(label='Series', backgroundColor=COLOR_TAB, borderColor=COLOR_TAB,
                data=[10, 29, 40] if randomData is False else data)


def buildDatasetPie(index=0, randomData=False, labelLenght=3):
    data = [random.randrange(100, 1000) for _ in range(labelLenght)]
    return dict(label=f'Series {index}', borderColor='#525252', backgroundColor=COLOR_TAB,
                data=[10, 29, 40] if randomData is False else data,
                borderWidth=1)


def buildDatasetDoughnut(index=0, randomData=False, labelLenght=4):
    exempleData = [895, 1478, 1267, 895, 734, 1056, 895, 1056]
    return dict(backgroundColor=COLOR_TAB,
                data=exempleData if randomData is False else [random.randrange(100, 150) for _ in range(labelLenght)])


def buildDatasetRadar(index=0, randomData=False, labelLenght=5):
    exempleData = [18, 10, 36, 36, 40]
    return dict(label=f'Series {index + 1}', fill=True,
                data=exempleData if randomData is False else [random.randrange(4, 50) for _ in range(labelLenght)],
                backgroundColor=COLOR_TAB[index], borderColor=COLOR_TAB[index],
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
                vbar_chart=buildDatasetBar)[tile_template](index=0, randomData=True, labelLenght=5)
