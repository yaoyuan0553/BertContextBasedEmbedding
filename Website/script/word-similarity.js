var xhr = new XMLHttpRequest();
var url = "http://127.0.0.1:5001/similarity_ranker";
xhr.open("POST", url, true);
xhr.setRequestHeader("Content-Type", "application/json");
xhr.onreadystatechange = dataReceiver;

function dataReceiver()
{
    var sampleWords = ["尚", "稍", "稍微", "比较", "略"];
    var sampleSims = [75.38, 69.90, 67.61, 65.64, 65.34];

    if (xhr.readyState === 4 && xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        console.log(data)
    }

    // return {words: sampleWords.reverse(), sims: sampleSims.reverse()};
}

/*
* json format:
* n - number of words to return [default: None]
* word - target to show similarities with
* category - category to show similarity from [default: None]
*/
function dataMaker(word, n, category)
{
    var data = {
        word: "还",
        n: 5,
        category: "#12程度浅"
    };

    return JSON.stringify(data);
}

function dataSender(data)
{
    xhr.send(data);
}


$(document).ready(function() {
    var myChart = echarts.init(document.getElementById('main'));
    option = {
        title : {
            text: '世界人口总量',
            subtext: '数据来自网络'
        },
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            },
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: true},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        xAxis : [
            {
                type : 'value',
                show : false,
                min: 0,
                max: 100
            }
        ],
        yAxis : [
            {
                type : 'category',
                data : ['巴西','印尼','美国','印度','中国','世界人口(万)']
            }
        ],
        series : [
            {
                name:'2011年',
                type:'bar',
                itemStyle : { normal: {label : {show: true, position: 'right', formatter: "{c}\%"}}},
                data:[18203, 23489, 29034, 104970, 131744, 630230]
            }
        ]
    };

    function updateBarGraph(dict)
    {
        option.yAxis[0].data = dict.words;
        option.series[0].data = dict.sims;
    }
    var sampleWords = ["尚", "稍", "稍微", "比较", "略"];
    var sampleSims = [75.38, 69.90, 67.61, 65.64, 65.34];
    var sampleData = {words: sampleWords, sims: sampleSims};

    updateBarGraph(sampleData);


    myChart.setOption(option);

    dataSender(dataMaker());
});
