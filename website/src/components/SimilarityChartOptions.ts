import echarts from 'echarts';

export let similarityChartOption: echarts.EChartOption<echarts.EChartOption.SeriesBar> = {
    // dataset: [{
    //     dimensions: ['word', 'similarityScore'],
    //     source: [
    //
    //     ],
    // }],
    title : {
        text: '词汇相似度排名',
    },
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow',        // 默认为直线，可选为：'line' | 'shadow'
        },
        // formatter: (params) => {
        //     // @ts-ignore
        //     return params[0].name + '<br/>' + params[0].seriesName + ': ' + params[0].value.toString() + '\%';
        // },
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: true},
            restore : {show: true},
            saveAsImage : {show: true},
        },
    },
    legend: [{
        show: true,
        data: [{
            name: '相似度',
            // 强制设置图形为圆。
            icon: 'circle',
            textStyle: {
                color: 'white',
                fontSize: 16,
            },
        }],
    }],
    xAxis : [
        {
            type : 'value',
            show : false,
            min: 0,
            max: 100,
        },
    ],
    yAxis : [
        {
            type : 'category',
            // data : [],
            axisLine : {show : false},
            axisTick : {show : false},
            axisLabel : {
                fontFamily: 'KaiTi_GB2312',
                fontWeight: 'bold',
                fontSize: 14,
            },
        },
    ],
    series : [
        {
            name: '相似度',
            type: 'bar',

            datasetIndex: 0,
            // data: [],
            label: {
                show: true,
                position: 'right',
                // formatter: (params: { value: { toFixed: (arg0: number) => { toString: () => string; }; }; }) => {
                //     return params.value.toFixed(2).toString() + '\%';
                // },
                fontFamily: 'Arial',
                fontWeight: 'bold',
                fontSize: 14,
            },
        },
    ],
    animationDurationUpdate: 800,
};
