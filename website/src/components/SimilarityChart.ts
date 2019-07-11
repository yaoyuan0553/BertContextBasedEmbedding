import * as echarts from 'echarts';
import {similarityChartOption as option} from '@/components/SimilarityChartOptions';

export default class SimilarityChart {
    public chart: echarts.ECharts;

    constructor(element: HTMLDivElement | HTMLCanvasElement, theme?: object | string)
    {
        this.chart = echarts.init(element, theme);
        this.chart.setOption(option);
    }

    private updateContainerHeight()
    {
        const op = this.chart.getOption();
        if (op === undefined) {
            return;
        }
        if (op.series === undefined) {
            return;
        }
        const barSeries: echarts.EChartOption.SeriesBar = op.series[0] as echarts.EChartOption.SeriesBar;
        const sims = barSeries.data;
        if (sims === undefined) {
            return;
        }
        const autoHeight = sims.length * 40 + 150;
        this.chart.getDom().style.height = autoHeight + 'px';
        // $(this.chart.getDom()).children()[0].style.height = 0;
        (this.chart.getDom().childNodes[0] as HTMLElement).style.height = autoHeight + 'px';
        (this.chart.getDom().childNodes[0].childNodes[0] as HTMLElement).setAttribute(
            'height', String(autoHeight));
        (this.chart.getDom().childNodes[0].childNodes[0] as HTMLElement).style.height = autoHeight + 'px';
        this.chart.resize();
    }

    public update(words: string[], sims: number[])
    {
        const newOption: echarts.EChartOption = {
            yAxis: [{data: words}],
            series: [{data: sims}],
        };
        this.chart.setOption(newOption);
        this.updateContainerHeight();
    }
}
