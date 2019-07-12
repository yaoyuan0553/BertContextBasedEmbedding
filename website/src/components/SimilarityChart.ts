import * as echarts from 'echarts';
import {similarityChartOption as option} from '@/components/SimilarityChartOptions';
import {ChalkTheme} from '@/components/EchartThemes';
import { WordSimilarityList } from '@/components/MessageDataTypes';
import YAxis = echarts.EChartOption.YAxis;

interface CatWordSimilarity {
    words: string[];
    similarities: number[];
}

export default class SimilarityChart {
    public chart: echarts.ECharts;

    public categories: string[] = [];
    public catWordSimilarity: CatWordSimilarity[] = [];
    public curCatIndex: number = 0;

    constructor(element: HTMLDivElement | HTMLCanvasElement, theme?: object | string)
    {
        this.chart = echarts.init(element, theme);
        this.chart.setOption(option);
    }

    private updateContainerHeight()
    {
        const dataSourceLen = this.catWordSimilarity[this.curCatIndex].words.length;
        const autoHeight = dataSourceLen * 45 + 150;
        this.chart.getDom().style.height = autoHeight + 'px';
        // $(this.chart.getDom()).children()[0].style.height = 0;
        (this.chart.getDom().childNodes[0] as HTMLElement).style.height = autoHeight + 'px';
        (this.chart.getDom().childNodes[0].childNodes[0] as HTMLElement).setAttribute(
            'height', String(autoHeight));
        (this.chart.getDom().childNodes[0].childNodes[0] as HTMLElement).style.height = autoHeight + 'px';
        this.chart.resize();
    }

    public update(wordSimByCat: Record<string, WordSimilarityList>)
    {
        this.curCatIndex = 0;
        this.categories = [];
        this.catWordSimilarity = [];
        let j = 0;
        for (let cat in wordSimByCat) {
            this.categories.push(cat);
            this.catWordSimilarity.push({words: [], similarities: []});
            for (let i = wordSimByCat[cat].length - 1; i >= 0; i--) {
                this.catWordSimilarity[j].words.push(wordSimByCat[cat][i].word);
                this.catWordSimilarity[j].
                    similarities.push(wordSimByCat[cat][i].similarityScore);
            }
            j++;
        }
        const newOption: echarts.EChartOption = {
            yAxis: [{data: this.catWordSimilarity[0].words}],
            series: [{name: this.categories[0], data: this.catWordSimilarity[0].similarities}],
            legend: {data: [{
                name: this.categories[0],
                textStyle: {
                    color: 'white',
                    fontSize: 16,
                },
            }]},
        };
        this.chart.setOption(newOption);
        this.updateContainerHeight();
    }

    public displayCategory(index: number)
    {
        if (index >= this.categories.length || index < 0) {
            return;
        }
        // let newOption: echarts.EChartOption = this.chart.getOption();
        // console.log('newOption', newOption);
        // (newOption.series![0] as echarts.EChartOption.SeriesBar).datasetIndex = index;
        let newOption: echarts.EChartOption = {
            yAxis: [{data: this.catWordSimilarity[index].words}],
            series: [{name: this.categories[index], data: this.catWordSimilarity[index].similarities}],
            legend: {data: [{
                name: this.categories[index],
                textStyle: {
                    color: 'white',
                    fontSize: 16,
                },
            }]},
            color: [ChalkTheme.color[index % ChalkTheme.color.length]],
        };
        this.chart.setOption(newOption);
        this.updateContainerHeight();
    }

    public nextCategory()
    {
        const oldCatIndex = this.curCatIndex;
        this.curCatIndex = this.categories.length === 0 ? 0 : (this.curCatIndex + 1) % this.categories.length;

        if (oldCatIndex !== this.curCatIndex) {
            this.displayCategory(this.curCatIndex);
        }
    }

    public prevCategory()
    {
        const oldCatIndex = this.curCatIndex;
        const len = this.categories.length;
        this.curCatIndex = len === 0 ? 0 : this.curCatIndex === 0 ? len - 1 : this.curCatIndex - 1;

        if (oldCatIndex !== this.curCatIndex) {
            this.displayCategory(this.curCatIndex);
        }
    }

    /* returns currently displayed category */
    public currentCategory()
    {
        // @ts-ignore
    }
}
