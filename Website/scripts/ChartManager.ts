import $ = require("jquery");
import echarts = require("echarts");
import {similarityChartOption as option} from "./SimilarityChartOptions";

export class ChartManager {
    chart: echarts.ECharts;

    constructor(element: HTMLDivElement | HTMLCanvasElement, theme?: object | string)
    {
        this.chart = echarts.init(element, theme);
        this.chart.setOption(option);
    }

    private updateContainerHeight()
    {
        let sims = (<echarts.EChartOption.SeriesBar>this.chart.getOption().series[0]).data;
        let autoHeight = sims.length * 40 + 150;
        this.chart.getDom().style.height = autoHeight + "px";
        // $(this.chart.getDom()).children()[0].style.height = 0;
        (<HTMLElement>this.chart.getDom().childNodes[0]).style.height = autoHeight + "px";
        (<HTMLElement>this.chart.getDom().childNodes[0].childNodes[0]).setAttribute(
            "height", String(autoHeight));
        (<HTMLElement>this.chart.getDom().childNodes[0].childNodes[0]).style.height = autoHeight + "px";
        this.chart.resize();
    }

    update(words: string[], sims: number[])
    {
        let newOption: echarts.EChartOption = {
            yAxis: [{data: words}],
            series: [{data: sims}]
        };
        this.chart.setOption(newOption);
        this.updateContainerHeight();
    }
}
