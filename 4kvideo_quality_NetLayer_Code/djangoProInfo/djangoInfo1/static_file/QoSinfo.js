/**
 * Created by zgr on 2017/1/2.
 */

//动态呈现重传乱序
function Retran() {
    // 基于准备好的dom，初始化echarts图表
    var myChart = echarts.init(document.getElementById('info3'));

    var option = {
        title : {
            text: '重传/乱序(%)',
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            show:true,
            data:['重传乱序'],
            textStyle: {
                color: '#fff'
            }
        },
        color:[
            '#FF3333',
        ],
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'line']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        dataZoom: {
            show: false,
            start: 0,
            end: 100
        },
        calculable : true,
        xAxis : [

            {
                type : 'category',
                boundaryGap : true,
                splitLine: {show: false},  //去除x轴网格线
                data : (function(){
                    var now = new Date();
                    var res = [];
                    var len = 100;
                    while (len--) {
                        res.unshift(now.toLocaleTimeString().replace(/^\D*/,''));
                        now = new Date(now - 2000);
                    }
                    return res;//开始是随机的数
                })()
            }
        ],
        yAxis : [
            {
                type : 'value',
                scale: true,
                splitLine: {show: false},  //去除y轴网格线
                precision:1,
                power:1,
                name : '%',
                boundaryGap: [0.2, 0.2],
                splitArea : {show : true}
            }
        ],
        series : [
            {
                name:'重传乱序率',
                type:'line',
                smooth:false,
                data: (function () {
                    var res = [];
                    var len = 100;
                    while (len--) {
                        res.push(Math.round(Math.random() * 0));
                    }
                    return res;
                })()
                //data:[]
            }
        ],
        calculable : false
    };

    // 为echarts对象加载数据
    myChart.setOption(option);

    var lastData = 11;
    var axisData;
    //clearInterval(timeTicket);
    timeTicket = setInterval(function () {
        //防止ajax，要异步async : true,
        $.ajax({
        url: '/getReTran/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        async:true,
        dataType:"json",
        success: function(data) {
            var retran = data.retran;
            var len = retran.length;
            if(len == 0)
            {
                axisData = (new Date()).toLocaleTimeString().replace(/^\D*/, '');
                // 动态数据接口 addData
                myChart.addData([
                [
                    0,        // 系列索引
                    -1, // 新增数据
                    //retran[i].reTran,
                    false,    // 新增数据是否从队列头部插入
                    false,     // 是否增加队列长度，false则自定删除原有数据，队头插入删队尾，队尾插入删队头
                    axisData  // 坐标轴标签
                ]
                ]);
            }else
            {
                for(var i = 0; i < len; ++i)
                {
                    axisData = (new Date()).toLocaleTimeString().replace(/^\D*/, '');
                    axisData = retran[i].reTranTIme;
                    // 动态数据接口 addData
                    myChart.addData([
                    [
                        0,        // 系列索引
                        //Math.round(Math.random() * 10), // 新增数据
                        retran[i].reTran,
                        false,    // 新增数据是否从队列头部插入
                        false,     // 是否增加队列长度，false则自定删除原有数据，队头插入删队尾，队尾插入删队头
                        axisData  // 坐标轴标签
                    ]
               ]);
                }
            }
        },
        failure: function(data) {
            alert('Got an error dude');
        }
    });
    }, 15000);


}


//用来显示重传界面
function showreTran(){
    var myChart = echarts.init(document.getElementById('info3'));

    var option = {
        title : {
            text: '重传/乱序(%)',
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            show:true,
            data:['重传乱序'],
            textStyle: {
                color: '#fff'
            }
        },
        color:[
            '#FF3333',
        ],
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'line']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        dataZoom: {
            show: false,
            start: 0,
            end: 100
        },
        calculable : true,
        xAxis : [

            {
                type : 'category',
                boundaryGap : true,
                splitLine: {show: false},  //去除x轴网格线
                data : (function(){
                    var now = new Date();
                    var res = [];
                    var len = 100;
                    while (len--) {
                        res.unshift(now.toLocaleTimeString().replace(/^\D*/,''));
                        now = new Date(now - 2000);
                    }
                    return res;//开始是随机的数
                })()
            }
        ],
        yAxis : [
            {
                type : 'value',
                scale: true,
                splitLine: {show: false},  //去除y轴网格线
                precision:1,
                power:1,
                name : '%',
                boundaryGap: [0.2, 0.2],
                splitArea : {show : true}
            }
        ],
        series : [
            {
                name:'重传乱序率',
                type:'line',
                smooth:false,
                data: []//(function () {
//                    var res = [];
//                    var len = 100;
//                    while (len--) {
//                        res.push(Math.round(Math.random() * 10));
//                    }
//                    return res;
//                })()
            }
        ],
        calculable : false
    };

    // 为echarts对象加载数据
    myChart.setOption(option);
}
//myChart.showLoading({
//    text: '正在努力加载中...'
//});    //数据加载完之前先显示一段简单的loading动画
//$(document).ready(function(){
//    $("#btndisplay").toggle(
//      function(){
//        $("#info1").css("display","block");
//        $("#info2").css("display","block");
//        $("#info3").css("display","block");
//        $("#calReTran").css("display","block");
//        showreTran();
//    },
//      function(){
//        $("#info1").css("display","none");
//        $("#info2").css("display","none");
//        $("#info3").css("display","none");
//        $("#calReTran").css("display","none");
//        }
//    );
//});



//流媒体，http码，TCP时间
function info1(){
    //利用ajax获取信息
    $.ajax({
        url: '/getInfoSource/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        async:true,
        success: function(data) {
            var soucre = data.source;
            var httpcode = data.httpcode;
            var len = httpcode.length;
            console.log(len);

            if(len == 0)
            {
                var tr1="<tr>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"</tr>";
                $("#info1mes").prepend(tr1);
            }
            else
            {
                var firstURL = soucre[0].urlAdd;
                if(firstURL == "b"){
                    for(var i = 0; i < len; i++)
                    {

                        var tr1="<tr>"+"<td>"+soucre[i+1].srcTodst+"</td>"+"<td>"+soucre[i+1].urlAdd+"</td>"+"<td>"+soucre[i+1].reqTIme+"</td>"+"<td>"+httpcode[i].httpCode+"</td>"+"<td>"+soucre[i+1].TCPtime+"</td>"+"</tr>";
                        $("#info1mes").prepend(tr1);
                    }
                }else
                {
                    for(var i = 0; i < len; i++)
                    {
                        var tr1="<tr>"+"<td>"+soucre[i].srcTodst+"</td>"+"<td>"+soucre[i].urlAdd+"</td>"+"<td>"+soucre[i].reqTIme+"</td>"+"<td>"+httpcode[i].httpCode+"</td>"+"<td>"+soucre[i].TCPtime+"</td>"+"</tr>";
                        $("#info1mes").prepend(tr1);
                    }
                }
           }
        },
        failure: function(data) {
            alert('Got an error dude');
        }
    });
}

//延时，带宽，抖动
function info2(){
    //利用ajax获取信息
    $.ajax({
        url: '/getInfoDelay/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        async:true,
        dataType:"json",
        success: function(data) {
            var bdelay = data.bdelay
            var len = bdelay.length;
            console.log(len)
            if(len == 0)
            {
               var tr1="<tr>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"</tr>";
               $("#info2mes").prepend(tr1);
            }
            else
            {
                for(var i = 0 ; i < len; i++)
                {
                    var tr1="<tr>"+"<td>"+bdelay[i].bandWidth+"</td>"+"<td>"+bdelay[i].delay+"</td>"+"<td>"+bdelay[i].jetter+"</td>"+"<td>"+bdelay[i].bdTIme+"</td>"+"</tr>";
                    $("#info2mes").prepend(tr1);
                }
            }
        },
        failure: function(data) {
            alert('Got an error dude');
        }
    });
}

$("#btndisplay").click(function(){
//    $("#info1").css("display","block");
//    $("#info2").css("display","block");
//    $("#info3").css("display","block");
//    $("#calReTran").css("display","block");
    $("#info1").fadeToggle("slow");
    $("#info2").fadeToggle("slow");
    $("#info3").fadeToggle("slow");
    //$("#calReTran").toggle();
    showreTran();
});

//监测Soucre
$("#btn1").click(function(){
    alert("监测1已启动");
    var set1 = setInterval(info1,13000);
});

//监测抖动
$("#btn2").click(function(){
    alert("监测2已启动");
    var set2 = setInterval(info2,4500);
});

//监测重传乱序
$("#btn4").click(function(){
     alert("监测3已启动");

});

$("#btn3").removeAttr("disabled");
//START 启动抓包分析
$("#btn3").click(function(){
    $("#btn3info").css("display","block");
    console.log("anay");
    $("#btn3").attr("disabled","disabled");
    $.ajax({
        url: '/startDetect/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        async:true,
        success: function(data) {
            alert(data);
        },
        failure: function(data) {
            alert('Got an error dude');
        }
    });

});

//启动重传乱序计算
$("#calReTran").click(function(){
    console.log("Re");
    $.ajax({
        url: '/startCalReTran/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        async:true,
        success: function(data) {
            alert(data);
        },
        failure: function(data) {
            alert('Got an error dude');
        }
    });
});


//导出数据库并清空
$("#btn5").click(function(){
    $("#uploadhdfs").css("display","block");
    $.ajax({
        url: '/outAndDelete/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        async:true,
        dataType:"json",
        success: function(data) {
            var info = data.out;
            if(info == 1)
            {
                $("#uploadhdfs").css("display","none");
                alert("mysql导出数据表成功");
                }
        },
        failure: function(data) {
            alert('Got an error dude');
        }
    });

});

//把数据传至hadoop平台
$("#btn6").click(function(){
    $("#uploadhdfs").css("display","block");
    $.ajax({
        url: '/upToHadoop/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        async:true,
        dataType:"json",
        success: function(data) {
            var info = data.out;
            if(info == 1)
            {
                $("#uploadhdfs").css("display","none");
                alert("传至hadoop平台成功");
                }
        },
        failure: function(data) {
            alert('Got an error dude');
        }
    });
});

$("#btn7").click(function(){
    var msg = "您真的确定要删除吗？\n\n请确认！";
    if (confirm(msg)==true){
        $("#uploadhdfs").css("display","block");
        $.ajax({
            url: '/deleteHadoop/',
            type: 'get', // This is the default though, you don't actually need to always mention it
            async:true,
            dataType:"json",
            success: function(data) {
                var info = data.out;
                if(info == 1)
                {
                    $("#uploadhdfs").css("display","none");
                    alert("清空大数据文件成功");
                    }
            },
            failure: function(data) {
                alert('Got an error dude');
            }
        });
    }else{
        return false;
    }
});
