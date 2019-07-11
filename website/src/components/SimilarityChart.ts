import * as echarts from 'echarts';
import {similarityChartOption as option} from '@/components/SimilarityChartOptions';
import { WordSimilarityList } from '@/components/MessageDataTypes';

export default class SimilarityChart {
    public chart: echarts.ECharts;

    public categories: string[] = [];
    public curCatIndex: number = 0;

    constructor(element: HTMLDivElement | HTMLCanvasElement, theme?: object | string)
    {
        this.chart = echarts.init(element, theme);
        this.chart.setOption(option);
    }

    private updateContainerHeight()
    {
        const op = this.chart.getOption();
        const dataSourceLen = (op.dataset! as any[])[0].source.length;
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
        let datasetList = [];
        for (let cat in wordSimByCat) {
            this.categories.push(cat);
            datasetList.push({source: wordSimByCat[cat].reverse()});
        }
        console.log(datasetList);

        const newOption: echarts.EChartOption = {
            dataset: datasetList,
        };
        this.chart.setOption(newOption);
        this.updateContainerHeight();
    }

    public displayCategory(index: number)
    {
        if (index >= this.categories.length || index < 0) {
            return;
        }

        let newOption: echarts.EChartOption = this.chart.getOption();
        console.log('newOption', newOption);
        (newOption.series![0] as echarts.EChartOption.SeriesBar).datasetIndex = index;
        this.chart.setOption(newOption);
        // this.updateContainerHeight();
    }

    public nextCategory()
    {
        const oldCatIndex = this.curCatIndex;
        this.curCatIndex = this.categories.length === 0 ? 0 : (this.curCatIndex + 1) % this.categories.length;

        if (oldCatIndex !== this.curCatIndex) {
            this.displayCategory(this.curCatIndex);
        }
        console.log(this.curCatIndex);
        console.log(this.chart.getOption());
    }

    public prevCategory()
    {
        const oldCatIndex = this.curCatIndex;
        this.curCatIndex = this.categories.length === 0 ? 0 : Math.abs(this.curCatIndex - 1) % this.categories.length;

        if (oldCatIndex !== this.curCatIndex) {
            this.displayCategory(this.curCatIndex);
        }
        console.log(this.curCatIndex);
        console.log(this.chart.getOption());
    }

    /* returns currently displayed category */
    public currentCategory()
    {
        console.log((this.chart.getOption().series![0] as echarts.EchartOption.SeriesBar).datasetIndex);
    }
}
