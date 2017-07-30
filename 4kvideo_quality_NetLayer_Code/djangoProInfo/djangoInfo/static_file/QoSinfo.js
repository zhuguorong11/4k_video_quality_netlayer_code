/**
 * Created by zgr on 2017/1/2.
 */
var ip = '';
var timeTicket;
/*=====================================================line==================================================================*/
//动态呈现重传乱序
function Retran() {
    var dicIP = new Array();
    dicIP['192.168.1.2'] = [[],[]];
    dicIP['192.168.1.3'] = [[],[]];
    dicIP['192.168.1.4'] = [[],[]];
    dicIP['192.168.1.6'] = [[],[]];
    dicIP['192.168.1.5'] = [[],[]];
    dicIP['192.168.1.7'] = [[],[]];
    dicIP['192.168.1.8'] = [[],[]];
    // 基于准备好的dom，初始化echarts图表
    console.log('start------------------------');
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
            data:['reTran'],
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
                //data:dateTime
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
                name: 'reTran',
                type:'line',
                smooth:false,
                data: (function () {
                    var res = [];
                    var len = 10;
                    while (len--) {
                        res.push(Math.round(Math.random() * 0));
                    }
                    return res;
                })()
                //data:dataSeries
            }
        ],
        calculable : false
    };

    // 为echarts对象加载数据
    myChart.setOption(option);
/*=======================================================================================================================*/
    var selectIp = ip;
    $.ajax({
        url: '/getReTran/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        async:true,
        data:{"selectIp":selectIp},
        dataType:"json",
        success: function(data) {
            //console.log();
            //var mydata = JSON.parse(data)
            var retran = data.retran;
            console.log(retran);
            var len = retran.length;
            if(len == 0)
            {
                var dateTime = (new Date()).toLocaleTimeString().replace(/^\D*/, '');
                dicIP[selectIp][0].push(dateTime);
                dicIP[selectIp][1].push(-0.1);
                console.log(dicIP[selectIp][0]);
                console.log(dicIP[selectIp][1]);

                myChart.setOption({
                    xAxis: {
                        data: dicIP[selectIp][0]
                    },
                    series:[    //填入系列（内容）数据
                        {
                        data: dicIP[selectIp][1]

                        }
                       ]
                });
            }else
            {
                for(var i = 0; i < len; ++i)
                {
                    dicIP[selectIp][0].push(retran[i].reTranTIme);
                    dicIP[selectIp][1].push(parseFloat(retran[i].reTran));
                    myChart.setOption({
                        xAxis: {
                            data:(function () {
                                return dicIP[selectIp][0];
                            })()
                        },
                        series:[    //填入系列（内容）数据
                            {
                            data: (function () {
                                return dicIP[selectIp][1];
                            })()
                            }
                           ]
                    });
                }
                console.log(dicIP[selectIp]);
            }
        },
        failure: function(data) {
            alert('Got an error dude');
        }
    });

/*=======================================================================================================================*/
    var lastData = 11;
    var axisData;
    clearInterval(timeTicket);
    //timeTicket = setInterval(ajaxReTran(ip,myChart),15000);
    timeTicket = setInterval(function () {
        //防止ajax，要异步async : true,
        var selectIp = ip;
        console.log("nowIP:"+selectIp);
        $.ajax({
            url: '/getReTran/',
            type: 'get', // This is the default though, you don't actually need to always mention it
            async:true,
            data:{"selectIp":selectIp},
            dataType:"json",
            success: function(data) {
                //console.log();
                //var mydata = JSON.parse(data)
                var retran = data.retran;
                console.log(retran);
                var len = retran.length;
                if(len == 0)
                {
                    var dateTime = (new Date()).toLocaleTimeString().replace(/^\D*/, '');
/*                    axisData = (new Date()).toLocaleTimeString().replace(/^\D*//*, '');
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
                    ]);*/
                    dicIP[selectIp][0].push(dateTime);
                    dicIP[selectIp][1].push(-1);
                    console.log(dicIP[selectIp][0]);
                    console.log(dicIP[selectIp][1]);

                    myChart.setOption({
                        xAxis: {
                            data: dicIP[selectIp][0]
                        },
                        series:[    //填入系列（内容）数据
                            {
                            data: dicIP[selectIp][1]

                            }
                           ]
                    });
                }else
                {
                    for(var i = 0; i < len; ++i)
                    {
/*                        axisData = (new Date()).toLocaleTimeString().replace(/^\D*//*, '');
                        axisData = retran[i].reTranTIme;
                        // 动态数据接口 addData
                        //console.log(axisData+"  " + retran[i].reTran);
                        myChart.addData([
                        [
                            0,        // 系列索引
                            //Math.round(Math.random() * 10), // 新增数据
                            retran[i].reTran,
                            false,    // 新增数据是否从队列头部插入
                            false,     // 是否增加队列长度，false则自定删除原有数据，队头插入删队尾，队尾插入删队头
                            axisData  // 坐标轴标签
                        ]
                   ]);*/
                        dicIP[selectIp][0].push(retran[i].reTranTIme);
                        dicIP[selectIp][1].push(parseFloat(retran[i].reTran));
/*                        dataSet[0].push(axisData);
                        dataSet[1].push(-0.4);*/
                        myChart.setOption({
                            xAxis: {
                                data:(function () {
                                    return dicIP[selectIp][0];
                                })()
                            },
                            series:[    //填入系列（内容）数据
                                {
                                data: (function () {
                                    return dicIP[selectIp][1];
                                })()
                                }
                               ]
                        });
                    }
                    console.log(dicIP[selectIp]);

                }
            },
            failure: function(data) {
                alert('Got an error dude');
            }
    });
    }, 8000);//every 8s to ajax


}


//用来显示重传界面
function showreTran(){
    var myChart = echarts.init(document.getElementById('info3'));

    var option = {
        title : {
            text: '重传/乱序(%)[-1代表暂时未有数据]',
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            show:true,
            data:['reTran'],
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
                name:'reTran',
                type:'line',
                smooth:false,
                data: []
/*                (function () {
                    var res = [];
                    var len = 100;
                    while (len--) {
                        res.push(Math.round(Math.random() * 10));
                    }
                    return res;
                })()*/
            }
        ],
        calculable : false
    };

    // 为echarts对象加载数据
    myChart.setOption(option);
}
/*=======================================================================================================================*/


/*myChart.showLoading({
    text: '正在努力加载中...'
});    //数据加载完之前先显示一段简单的loading动画
$(document).ready(function(){
    $("#btndisplay").toggle(
      function(){
        $("#info1").css("display","block");
        $("#info2").css("display","block");
        $("#info3").css("display","block");
        $("#calReTran").css("display","block");
        showreTran();
    },
      function(){
        $("#info1").css("display","none");
        $("#info2").css("display","none");
        $("#info3").css("display","none");
        $("#calReTran").css("display","none");
        }
    );
});*/


/*==========================================================table update=============================================================*/
//流媒体，http码，TCP时间
function info1(){
    //利用ajax获取信息
    var selectIp = ip;
    $.ajax({
        url: '/getInfoSource/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        async:true,
        data:{"selectIp":selectIp},
        success: function(data) {
            var soucre = data.source;
            var httpcode = data.httpcode;
            var len = httpcode.length;
            console.log(len);
            console.log(data)
            if(len == 0)
            {
                var tr1="<tr class='mytr'>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"</tr>";
                $("#info1mes").prepend(tr1);
            }
            else
            {
//                var firstURL = soucre[0].urlAdd;
//                if(firstURL == "b"){
//                    for(var i = 0; i < len; i++)
//                    {
//
//                        var tr1="<tr>"+"<td>"+soucre[i+1].srcTodst+"</td>"+"<td>"+soucre[i+1].urlAdd+"</td>"+"<td>"+soucre[i+1].reqTIme+"</td>"+"<td>"+httpcode[i].httpCode+"</td>"+"<td>"+soucre[i+1].TCPtime+"</td>"+soucre[i+1].ipPlay+"</td>"+"</tr>";
//                        $("#info1mes").prepend(tr1);
//                    }
//                }else
//                {
//                    for(var i = 0; i < len; i++)
//                    {
//                        var tr1="<tr>"+"<td>"+soucre[i].srcTodst+"</td>"+"<td>"+soucre[i].urlAdd+"</td>"+"<td>"+soucre[i].reqTIme+"</td>"+"<td>"+httpcode[i].httpCode+"</td>"+"<td>"+soucre[i].TCPtime+"</td>"+"</tr>";
//                        $("#info1mes").prepend(tr1);
//                    }
//                }
                var sourceLen = soucre.length;
                var bcount = 0
                for(var i = 0; i < sourceLen;i++)
                {
                    var URL = soucre[i].urlAdd;//take away
                    if(URL == "b")
                    {
                        ++bcount;
                    }
                }
                for(var i = bcount; i < (len + bcount); ++i)
                {
                    var tr1="<tr class='mytr'>"+"<td>"+soucre[i].srcTodst+"</td>"+"<td>"+soucre[i].urlAdd+"</td>"+"<td>"+soucre[i].reqTIme+"</td>"+"<td>"+httpcode[i-bcount].httpCode+"</td>"+"<td>"+soucre[i].TCPtime+"</td>"+"<td>"+soucre[i].ipPlay+"</td>"+"</tr>";
                    $("#info1mes").prepend(tr1);
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
    var selectIp = ip;
    $.ajax({
        url: '/getInfoDelay/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        async:true,
        data:{"selectIp":selectIp},
        dataType:"json",
        success: function(data) {
            var bdelay = data.bdelay
            var len = bdelay.length;
            console.log(len)
            if(len == 0)
            {
               var tr1="<tr class='mytr'>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"<td>"+"暂无数据"+"</td>"+"</tr>";
               $("#info2mes").prepend(tr1);
            }
            else
            {
                for(var i = 0 ; i < len; i++)
                {
                    var tr1="<tr class='mytr'>"+"<td>"+bdelay[i].bandWidth+"</td>"+"<td>"+bdelay[i].delay+"</td>"+"<td>"+bdelay[i].jetter+"</td>"+"<td>"+bdelay[i].bdTIme+"</td>"+"<td>"+bdelay[i].ipPlay+"</td>"+"</tr>";
                    $("#info2mes").prepend(tr1);
                }
            }
        },
        failure: function(data) {
            alert('Got an error dude');
        }
    });
}
/*=======================================================================================================================*/

/*==================================================new=====================================================================*/
var psnrIp;
//获得视频信息
function info3(){
     //利用ajax获取信息
    var selectIp = ip;
    $.ajax({
        url: '/getVideoInfo/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        async:true,
        //data:{"selectIp":selectIp},
        dataType:"json",
        success: function(data) {
            var videoinfos = data.videoinfo;
            var len = videoinfos.length;
            console.log(len);
            if(len != 0)
            {
                var videoinfo = videoinfos[0];
                $("#filename").text(videoinfo.filename);
                $("#resolution").text(videoinfo.width+''+'*'+''+videoinfo.height);
                $("#framerate").text(videoinfo.framerate);
                $("#videoInfoIP").text(videoinfo.ip);
                psnrIp = videoinfo.ip;
            }
        },
        failure: function(data) {
            alert('Got an error dude');
        }
    });
}

//获得视频psnr
function info4(){
     //利用ajax获取信息
    var selectIp = ip;
    var psnrNowIP = psnrIp;
    $.ajax({
        url: '/getVideoQuqlity/',
        type: 'get', // This is the default though, you don't actually need to always mention it
        async:true,
        //data:{"selectIp":selectIp},
        dataType:"json",
        success: function(data) {
            var psnrs = data.psnrinfo;
            var ppp = data.pppp;
            var len = psnrs.length;
            console.log(psnrs);
            console.log(len);
            console.log(ppp);
            if(len != 0)
            {
                if(len == 2)
                {
                    console.log(psnrNowIP);
                    var filename1 = psnrs[0].filename;
                    var filename2 = psnrs[1].filename;
                    if(filename1 == filename2)
                    {
                        var psnr1 = psnrs[0].psnr;
                        var psnr2 = psnrs[1].psnr;
                        console.log(psnr2);
                        $("#psnr").text(psnr2);
                        if(psnr1 >= 18 && psnr2 >= 18)
                        {
                            $("#videoquality").text("差");
                            alert(psnrNowIP+":当前视频质量状况较差");
                        }else if(psnr1 <= 15 && psnr2 <= 15)
                        {
                            $("#videoquality").text("好");
                        }else
                        {
                            $("#videoquality").text("一般");
                        }
                    }else
                    {
                        var psnr = psnrs[1];
                        var psnrValue = 9//psnr.psnr;
                        $("#psnr").text(psnrValue);
                        var psnrValue = parseInt(psnrValue);
                        if(psnrValue >= 18)
                        {
                            $("#videoquality").text("差");
                            alert(psnrNowIP + ":当前视频质量状况较差");
                        }else if(psnrValue <= 15)
                        {
                            $("#videoquality").text("好");
                        }else{
                            $("#videoquality").text("一般");
                        }
                    }

                }else
                {
                    var psnr = psnrs[0];
                    var psnrValue = psnr.psnr;
                    $("#psnr").text(psnrValue);
                    var psnrValue = parseInt(psnrValue);
                    if(psnrValue >= 27)
                    {
                        $("#videoquality").text("差");
                    }else if(psnrValue <= 15)
                    {
                        $("#videoquality").text("好");
                    }else{
                        $("#videoquality").text("一般");
                    }
                }

//                $("#videoquality").text(psnrValue[0]);
            }
        },
        failure: function(data) {
            alert('Got an error dude');
        }
    });
}
/*=======================================================================================================================*/

/*===================================================btn event====================================================================*/
$("#btndisplay").click(function(){
    $("#info1").fadeToggle("slow");
    $("#info2").fadeToggle("slow");
    $("#info3").fadeToggle("slow");
    $("#ipinfo").fadeToggle("slow");
    $("#videoInfo").fadeToggle("slow");
    showreTran();
});

//监测Soucre
$("#btn1").click(function(){
    alert("监测1已启动");
    info1();
    var set1 = setInterval(info1,6500);
});

//监测抖动
$("#btn2").click(function(){
    alert("监测2已启动");
    info2();
    var set2 = setInterval(info2,4500);
});

//监测重传乱序
$("#btn4").click(function(){
     alert("监测3已启动");
     Retran();
});



/*$("#btn3").removeAttr("disabled");
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

});*/

/*启动重传乱序计算
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
});*/


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

//启动视频应用层打监视
$("#videoInfoShow").click(function(){
    alert("视频质量信息显示");
    var set4 = setInterval(info4,2200);
    var set3 = setInterval(info3,1000);
});
/*=======================================================================================================================*/

//ipchange
function ipChange(){
    var select = document.getElementById("s0");
    ip = select.options[select.selectedIndex].value;
    $("#ipinfo").text(ip);
    $("#ipInput").val(ip);
    $("#videoInfoIP").text(ip);
    console.log(ip);
    //filter table
//    $(".table-body table tbody tr .mytr")
//         .hide()
//         .filter(":contains('"+ip+"')")
//         .show();
    $(".mytr")
     .hide()
     .filter(":contains('"+ip+"')")
     .show();
}

//default option
function ipDefalut(){
    var select = document.getElementById("s0");
    ip = select.options[select.selectedIndex].value;
    $("#ipinfo").text(ip);
}

$("#ipInput").blur(function(){
    var selectVal = $(this).val();
    $("#ipinfo").text(selectVal);
    //$("#s0").find("option[text='"+($(this).val())+"']").attr("selected", "selected");
    $("#s0 option").each(function(){
        if($(this).text() == selectVal){
            $(this).attr({"selected":true});
        }else{
            $(this).attr({"selected":false});
        }
    });
    console.log(($(this).val()));
    ip = $(this).val();
//    $(".table-body table tbody tr")
//       .hide()
//       .filter(":contains('"+( $(this).val() )+"')")
//       .show();
    $(".mytr")
     .hide()
     .filter(":contains('"+ip+"')")
     .show();
});



