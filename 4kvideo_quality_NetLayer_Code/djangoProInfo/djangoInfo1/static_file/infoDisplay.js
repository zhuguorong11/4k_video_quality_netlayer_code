
//当点击时候，在模态框中展示出带宽、延时信息
$("#infoDisplay").click(function(e){
    var bandWidth = [];
    var delay = [];
    var jetter = [];
    var timeinfo = [];
    $.ajax({
            type: "GET",
            url: "/static_file/data/17_03_22_02_43_24packetInfo_bandwidth.txt",
            dataType: "text",
            success: function(rs) {
                var lines = rs.split("\r\n");

                for(var i = 0; i < lines.length; ++i)
                {
                    var line = lines[i];
                    var infos = line.split(",")
                    bandinfo = infos[1];
                    delayinfo = infos[2];
                    jetterinfo = infos[3];
                    time = infos[4];
                    if(typeof(bandinfo)=="undefined")
                    {
                        continue;
                        //bandinfo = "0";
                    }
                    if(typeof(delayinfo)=="undefined")
                    {
                        continue;
                        //delayinfo = "0";
                    }
                    if(typeof(jetterinfo)=="undefined")
                    {
                        continue;
                        //jetterinfo = "0";
                    }
                    if(typeof(time)=="undefined")
                    {
                        continue;
                        //time = "0";
                    }
                    bandWidth.push(bandinfo);
                    delay.push(delayinfo);
                    jetter.push(jetterinfo);
                    timeinfo.push(time);
                }
                console.log(bandWidth);
                console.log(delay);
                console.log(jetter);
                console.log(timeinfo);

                var bandwidthChart = echarts.init(document.getElementById('bandwidth'));
                var option1 = {
                    title: {      //标题组件
                        text: '带宽状况(MB/s)'
                    },
                    tooltip: {    //提示框组件
                        trigger: 'axis'
                    },
                    legend: {     //图例组件
                        show:true,
                        data:['带宽'],
                        textStyle: {
                            color: '#fff'
                        }
                    },
                    toolbox: {     //工具栏
                        show:true,
                        feature: {
                            saveAsImage: {}
                        }
                    },
                    xAxis: {       //直角坐标系 grid 中的 x 轴
                        type: 'category',
                        boundaryGap: false,
                        data: timeinfo
                    },
                    yAxis: {       //直角坐标系 grid 中的 y 轴
                        type: 'value'
                    },
                    series: [      //系列列表
                        {
                            name: '带宽',
                            type: 'line',
                            //stack: '总量',
                            data: bandWidth

                        }
                    ]
                };
                bandwidthChart.setOption(option1);

                var delayChart = echarts.init(document.getElementById('delay'));
                var option2 = {
                    title: {      //标题组件
                        text: '延时状况(ms)'
                    },
                    tooltip: {    //提示框组件
                        trigger: 'axis'
                    },
                    legend: {     //图例组件
                        show:true,
                        data:['延时'],
                        textStyle: {
                            color: '#fff'
                        }
                    },
                    toolbox: {     //工具栏
                        show:true,
                        feature: {
                            saveAsImage: {}
                        }
                    },
                    xAxis: {       //直角坐标系 grid 中的 x 轴
                        type: 'category',
                        boundaryGap: false,
                        data: timeinfo
                    },
                    yAxis: {       //直角坐标系 grid 中的 y 轴
                        type: 'value'
                    },
                    series: [      //系列列表
                        {
                            name: '延时',
                            type: 'line',
                            stack: '总量',
                            data: delay

                        }
                    ]
                };
                delayChart.setOption(option2);

                var jetterChart = echarts.init(document.getElementById('jetter'));
                var option3 = {
                    title: {      //标题组件
                        text: '抖动状况(ms)'
                    },
                    tooltip: {    //提示框组件
                        trigger: 'axis'
                    },
                    legend: {     //图例组件
                        show:true,
                        data:['抖动'],
                        textStyle: {
                            color: '#fff'
                        }
                    },
                    toolbox: {     //工具栏
                        show:true,
                        feature: {
                            saveAsImage: {}
                        }
                    },
                    xAxis: {       //直角坐标系 grid 中的 x 轴
                        type: 'category',
                        boundaryGap: false,
                        data: timeinfo
                    },
                    yAxis: {       //直角坐标系 grid 中的 y 轴
                        type: 'value'
                    },
                    series: [      //系列列表
                        {
                            name: '抖动',
                            type: 'line',
                            stack: '总量',
                            data: jetter

                        }
                    ]
                };
                jetterChart.setOption(option3);
             },
            error: function() {
               alert("error");
             }
        });
    //$("#bandwidth").append("asdasdasdsad");
    //读取文件内容
//    ReadText("file:///var/lib/mysql-files/packetInfo_bandwidth.txt");
//    var bandwidthChart = echarts.init(document.getElementById('bandwidth'));
//    //参数设置
//
});

