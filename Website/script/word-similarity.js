let xhr = new XMLHttpRequest();
let url = "http://0.0.0.0:5001/similarity_ranker";

$(document).ready(function() {
    let wordInputField = $('.wordForm .chosen-value')[0];
    let wordDropdown = $('.wordForm .value-list')[0];
    let catInputField = $('.categoryForm .chosen-value')[0];
    let catDropdown = $('.categoryForm .value-list')[0];
    let rankCount = $('.rankCountForm input.rankCount')[0];

    function updateDropdownEvents(inputField, dropdown) {
        var dropdownItems = dropdown.querySelectorAll('li');

        var valueArray = [];
        dropdownItems.forEach(function (item) {
            valueArray.push(item.textContent);
        });

        var closeDropdown = function closeDropdown() {
            dropdown.classList.remove('open');
        };

        inputField.addEventListener('input', function () {
            dropdown.classList.add('open');
            var inputValue = inputField.value;
            if (inputValue.length > 0) {
                for (var j = 0; j < valueArray.length; j++) {
                    if (!(inputValue.substring(0, inputValue.length)
                        === valueArray[j].substring(0, inputValue.length))) {
                        dropdownItems[j].classList.add('closed');
                    } else {
                        dropdownItems[j].classList.remove('closed');
                    }
                }
            } else {
                for (var i = 0; i < dropdownItems.length; i++) {
                    dropdownItems[i].classList.remove('closed');
                }
            }
        });

        dropdownItems.forEach(function (item) {
            item.addEventListener('click', function (evt) {
                inputField.value = item.textContent;
                dropdownItems.forEach(function (dropdown) {
                    dropdown.classList.add('closed');
                });
            });
        });

        var origPlaceHolder = inputField.placeholder;

        inputField.addEventListener('focus', function () {
            inputField.placeholder = '输入以筛选';
            dropdown.classList.add('open');
            dropdownItems.forEach(function (dropdown) {
                dropdown.classList.remove('closed');
            });
        });

        inputField.addEventListener('blur', function () {
            inputField.placeholder = origPlaceHolder;
            dropdown.classList.remove('open');
        });
    }
    // var inputField = $('.categoryForm .chosen-value')[0];
    // var dropdown = $('.categoryForm .value-list')[0];

    updateDropdownEvents(catInputField, catDropdown);

    function addDropdownEvent(inputField, dropdown)
    {
        document.addEventListener('click', function (evt) {
            var isDropdown = dropdown.contains(evt.target);
            var isInput = inputField.contains(evt.target);
            if (!isDropdown && !isInput) {
                dropdown.classList.remove('open');
            }
        });
    }

    addDropdownEvent(catInputField, catDropdown);
    addDropdownEvent(wordInputField, wordDropdown);

    xhr.onreadystatechange = dataReceiver;

    function updateCategoryList(catList)
    {
        //var optionList = [{text: '类别', value: 'null', selected: true}];
        categoryOptions.add(new Option('类别', 'null', true));
        catList.forEach(cat =>
            categoryOptions.add(new Option(cat, cat))
        );
    }
    function updateDropdownForm(inputField, dropdown, list)
    {
        dropdown.innerHTML = "";
        autoLi = document.createElement('li');
        autoLi.innerText = '[自动]';
        dropdown.appendChild(autoLi);
        list.forEach(function(cat) {
                var li = document.createElement('li');
                li.innerText = cat;
                dropdown.appendChild(li);
            }
        );
        updateDropdownEvents(inputField, dropdown);
        // dropdownItems.forEach(function (item) {
        //    item.
        // });
    }
    // updateCategoryForm(['1', '哈哈', '后悔']);

    function dataReceiver()
    {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            console.log(data);

            var newGraphData = {
                "words": [],
                "sims": []
            };
            if (data.hasOwnProperty('info')) {
                // console.log(data.info);
                if (data.info.hasOwnProperty('categories')) {
                    // updateCategoryList(data.info.categories);
                    updateDropdownForm(catInputField, catDropdown, data.info.categories);
                    updateDropdownForm(wordInputField, wordDropdown, data.info.words);
                }
            }
            // console.log(data.sim_ranks);
            for (let cat in data.sim_ranks) {
                if (data.sim_ranks.hasOwnProperty(cat)) {
                    // console.log(cat);
                    for (var i = data.sim_ranks[cat].length - 1; i >= 0; i--) {
                        // console.log(data[cat][i]);
                        newGraphData.words.push(data.sim_ranks[cat][i]['word']);
                        newGraphData.sims.push(data.sim_ranks[cat][i]['similarityScore']);
                    }
                }
            }
            // console.log(newGraphData);
            updateBarGraph(newGraphData)
        }
    }

    /*
    * json format:
    * n - number of words to return [default: None]
    * word - target to show similarities with
    * category - category to show similarity from [default: None]
    */
    function makeData(first = false)
    {
        if (first)
            return JSON.stringify({request_info: first});

        var cat = catInputField.value;
        var word = wordInputField.value;
        var n = rankCount.value;
        console.log(n !== "");
        console.log(n);
        if (n !== "" && isNaN(n)) {
            alert("显示数量必须为数字!");
            return null;
        }
        if (word === "")
            return null;
        if (cat === "[自动]" || cat === "")
            cat = 'null';
        if (n === "")
            n = 'null';
        else
            n = Number(n);

        var data = {
            word: word,
            n: n,
            category: cat,
            request_info: first
        };

        return JSON.stringify(data);
    }

    function dataSender(data)
    {
        // if data is null do nothing
        if (data === null)
            return;
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");

        console.log(data);
        xhr.send(data);
    }

    let myChart = echarts.init(document.getElementById('main'));
    option = {
        title : {
            text: '词汇相似度排名',
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
                data : [],
                axisLine : {show : false},
                axisTick : {show : false},
                axisLabel : {
                    fontFamily: 'Microsoft YaHei',
                    fontWeight: 'bold',
                    fontSize: 14
                }
            }
        ],
        series : [
            {
                name:'相似度',
                type:'bar',
                itemStyle : { normal: {label : {show: true, position: 'right', formatter: function(params) {console.log(params);}}}},
                data:[]
            }
        ],
        animationDurationUpdate: 800
    };

    function updateBarGraph(dict)
    {
        newOption = {
            yAxis: [
                {
                    data : dict.words
                }
            ],
            series: [
                {
                    data: dict.sims
                }
            ]
        };

        myChart.setOption(newOption);

        sims = myChart.getOption().series[0].data;

        console.log(sims.length);
        let autoHeight = sims.length * 40 + 150;
        myChart.getDom().style.height = autoHeight + "px";
        myChart.getDom().childNodes[0].style.height = autoHeight + "px";
        myChart.getDom().childNodes[0].childNodes[0].setAttribute("height", autoHeight);
        myChart.getDom().childNodes[0].childNodes[0].style.height = autoHeight + "px";
        myChart.resize();
    }

    // updateBarGraph(sampleData);

    myChart.setOption(option);

    var loading = function(e) {
        e.preventDefault();
        e.stopPropagation();
        e.target.classList.add('loading');
        e.target.setAttribute('disabled','disabled');
        setTimeout(function(){
            e.target.classList.remove('loading');
            e.target.removeAttribute('disabled');
        },1500);
    };

    var computeButton = $('button.compute-ranking')[0];
    computeButton.onclick = function (e) {
        loading(e);
        dataSender(makeData());
    };

    dataSender(makeData(true));
});
