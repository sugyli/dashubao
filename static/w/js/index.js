$(document).ready(function()
{
    islogin();

});
function islogin() {
     var is_login = $.fn.cookie("is_login");
     if(is_login == 1 && document.getElementById("ajax_login")){
        $.ajax({
            cache: false,
            type: "post",
            url:config.verifylogin_url,
            data:'',
            async: true,
            beforeSend:function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", config.csrf_token);
            },
            success: function(result) {
                if(result.status == 'success'){
                    var data = result.data
                    $("#ajax_login").html(getloginhtml(data));
                }
            },
            error: function(jqXHR, textStatus, errorThrown){

                /*弹出jqXHR对象的信息*/
                console.log(jqXHR.responseText);
                console.log(jqXHR.status);
                console.log(jqXHR.readyState);
                console.log(jqXHR.statusText);
                /*弹出其他两个参数的信息*/
                console.log(textStatus);
                console.log(errorThrown);
            }
        });

     }

}

function getloginhtml(data) {

    var html =  '<ul>';
        html += '<li>'+ data.username +'</li>';
        html += '<li>等级：'+ data.caption +'</li>';
        html += '<li><a href="'+ config.userindex_url+'" target="_top">用户中心</a></li>';
        if(data.message > 0){
           html += '<li><a href="'+ config.message_url +'" style="color:red;">您有消息</a>';
        }
        html += '<li><a href="'+ config.logout_url +'?next='+ config.thiurl +'" target="_self">退出登录</a></li>';
        html += '</ul>';

    return html

}
$('#inpulogin').on('click', function(){

  var data = {
      'username': $.trim(document.getElementById('username').value),
      'password': $.trim(document.getElementById('password').value),
  };
  var _self = $(this);
  $.ajax({
        cache: false,
        type: "post",
        url:config.verifylogin_url,
        data:data,
        async: true,
        beforeSend:function(xhr, settings){
            layer.open({type: 2,shadeClose: true});
            xhr.setRequestHeader("X-CSRFToken", config.csrf_token);
            _self.val("加载中");
            _self.attr('disabled',true);
        },
        success: function(result) {
            layer.closeAll();
            if(result.username){
                showmsg(result.username)
            }else if(result.password){
                showmsg(result.password)
            }else if(result.status == 'success'){
                var data = result.data
                $("#ajax_login").html(getloginhtml(data));
            }else if(result.msg){
                showmsg(result.msg)
            }

        },
        complete: function(XMLHttpRequest){
            _self.val('登录');
            _self.removeAttr("disabled");

        },
        error: function(jqXHR, textStatus, errorThrown){
            layer.closeAll();
            /*弹出jqXHR对象的信息*/
            console.log(jqXHR.responseText);
            console.log(jqXHR.status);
            console.log(jqXHR.readyState);
            console.log(jqXHR.statusText);
            /*弹出其他两个参数的信息*/
            console.log(textStatus);
            console.log(errorThrown);
        }
    });

});


var content = function () {
    var date = 7;
    $("#screen").click(function() {
        var b = $("#screen").parent().parent().children(".select");
        b.show()
    });
    $("#screen1").click(function() {
        var b = $("#screen").parent().parent().children(".select");
        b.show()
    });
    $("#screen").parent().parent().children(".select").children("p").each(function() {
        $(this).click(function() {
            $("#screen").val($(this).html());
            $("#screen").parent().parent().children(".select").hide();
            var b = $("#screen").val();
            $.fn.cookie("screen", b, {
                path: "/",
                expires: date
            });
            a.start()
        })
    });

    $("#background").click(function() {
        var b = $("#background").parent().parent().children(".select");
        b.show()
    });
    $("#background1").click(function() {
        var b = $("#background1").parent().parent().children(".select");
        b.show()
    });
    $(".select").parent().each(function() {
        $(this).mouseover(function() {
            $(this).children(".select").show()
        })

        $(this).mouseout(function() {
            $(this).children(".select").hide()
        })
    });


    $("#background").parent().parent().children(".select").children("p").each(function() {
        $(this).click(function() {
            $("#background").val($(this).html());
            $("#background").parent().parent().children(".select").hide();
            //$(".ydleft").removeClass($("#background2").val());
            $("body").removeClass($("#background2").val());
            $("body").attr("style", "");
            //$(".ydleft").attr("style", "");
            $("#background2").val($(this).attr("class"));
            //$(".ydleft").addClass($(this).attr("class"));
            $("body").addClass($(this).attr("class"))
        })
    });
    $("#fontSize").click(function() {
        var b = $("#fontSize").parent().parent().children(".select");
        b.show()
    });
    $("#fontSize1").click(function() {
        var b = $("#fontSize1").parent().parent().children(".select");
        b.show()
    });
    $("#fontSize").parent().parent().children(".select").children("p").each(function() {
        $(this).click(function() {
            $("#fontSize").val($(this).html());
            $("#fontSize").parent().parent().children(".select").hide();
            $(".yd_text2").removeClass($("#fontSize2").val());
            $("#fontSize2").val($(this).attr("class"));
            $(".yd_text2").addClass($(this).attr("class"))
        })
    });
    $("#fontFamily").click(function() {
        var b = $("#fontFamily").parent().parent().children(".select");
        b.show()
    });
    $("#fontFamily1").click(function() {
        var b = $("#fontFamily1").parent().parent().children(".select");
        b.show()
    });
    $("#fontFamily").parent().parent().children(".select").children("p").each(function() {
        $(this).click(function() {
            $("#fontFamily").val($(this).html());
            $("#fontFamily").parent().parent().children(".select").hide();
            $(".yd_text2").removeClass($("#fontFamily2").val());
            $("#fontFamily2").val($(this).attr("class"));
            $(".yd_text2").addClass($(this).attr("class"))
        })
    });
    $("#fontColor").click(function() {
        var b = $("#fontColor").parent().parent().children(".select");
        b.show()
    });
    $("#fontColor1").click(function() {
        var b = $("#fontColor1").parent().parent().children(".select");
        b.show()
    });
    $("#fontColor").parent().parent().children(".select").children("p").each(function() {
        $(this).click(function() {
            $("#fontColor").val($(this).html());
            $("#fontColor").parent().parent().children(".select").hide();
            $(".yd_text2").removeClass($("#fontColor2").val());
            $("#fontColor2").val($(this).attr("class"));
            $(".yd_text2").addClass($(this).attr("class"))
        })
    });
    $("#saveButton").click(function() {
        $.fn.cookie("screen", $("#screen").val(), {
            path: "/",
            expires: date
        });
        $.fn.cookie("background", $("#background2").val(), {
            path: "/",
            expires: date
        });
        $.fn.cookie("fontSize", $("#fontSize2").val(), {
            path: "/",
            expires: date
        });
        $.fn.cookie("fontColor", $("#fontColor2").val(), {
            path: "/",
            expires: date
        });
        $.fn.cookie("fontFamily", $("#fontFamily2").val(), {
            path: "/",
            expires: date
        });

        showmsg('保存成功')

    });
    $("#recoveryButton").click(function() {
        $("body").removeClass($.fn.cookie("background"));
        $("body").removeClass($("#background2").val());
        //$(".ydleft").removeClass($("#background2").val());
        //$(".ydleft").removeClass($.fn.cookie("background"));
        $("body").attr("style", "background:#fff");
        //$(".ydleft").attr("style", "background:#FFF");
        $(".yd_text2").removeClass($("#background2").val());
        $(".yd_text2").removeClass($("#fontSize2").val());
        $(".yd_text2").removeClass($.fn.cookie("fontSize"));
        $(".yd_text2").removeClass($("#fontColor2").val());
        $(".yd_text2").removeClass($.fn.cookie("fontColor"));
        $(".yd_text2").removeClass($("#fontFamily2").val());
        $(".yd_text2").removeClass($.fn.cookie("fontFamily"));
        $.fn.cookie("background", "", {
            path: "/",
            expires: date
        });
        $.fn.cookie("fontSize", "", {
            path: "/",
            expires: date
        });
        $.fn.cookie("fontColor", "", {
            path: "/",
            expires: date
        });
        $.fn.cookie("fontFamily", "", {
            path: "/",
            expires: date
        });
        $("#screen").val("滚屏");
        $("#background").val("背景");
        $("#fontColor").val("字色");
        $("#fontFamily").val("字体");
        $("#fontSize").val("字号")
    });

    var a = (function() {
        var d;
        var g;
        var f;
        function c() {
            g = setInterval(b, 40);
            try {
                if (document.selection) {
                    document.selection.empty()
                } else {
                    var h = document.getSelection();
                    h.removeAllRanges()
                }
            } catch(j) {}
        }
        function b() {
            d = document.documentElement.scrollTop || document.body.scrollTop;
            if ($.fn.cookie("screen") != null) {
                d = d + parseInt($.fn.cookie("screen"))
            }
            window.scroll(0, d);
            f = document.documentElement.scrollTop || document.body.scrollTop;
            if (d != f) {
                e()
            }
        }
        function e() {
            clearInterval(g)
        }
        return {
            start: c,
            stop: e
        }
    })();
    jQuery(document).dblclick(a.start);
    jQuery(document).mousedown(a.stop);


    if ($.fn.cookie("screen") != null && $.fn.cookie("screen") != "") {
        $("#screen").val($.fn.cookie("screen"))
    } else {
        $("#screen").val("滚屏")
    }
    if ($.fn.cookie("fontSize") != null && $.fn.cookie("fontSize") != "") {
        $(".yd_text2").addClass($.fn.cookie("fontSize"));
        size = $.fn.cookie("fontSize").replace("fon_", "");
        size += "px";

        $("#fontSize").val(size);
        $("#fontSize2").val($.fn.cookie("fontSize"))
    }
    if ($.fn.cookie("background") != null && $.fn.cookie("background") != "") {
        var b = "背景";
        if ($.fn.cookie("background") == "bg_lan") {
            b = "淡蓝"
        }
        if ($.fn.cookie("background") == "bg_huang") {
            b = "明黄"
        }
        if ($.fn.cookie("background") == "bg_lv") {
            b = "淡绿"
        }
        if ($.fn.cookie("background") == "bg_fen") {
            b = "红粉"
        }
        if ($.fn.cookie("background") == "bg_bai") {
            b = "白色"
        }
        if ($.fn.cookie("background") == "bg_hui") {
            b = "灰色"
        }
        if ($.fn.cookie("background") == "bg_hei") {
            b = "漆黑"
        }
        if ($.fn.cookie("background") == "bg_cao") {
            b = "草绿"
        }
        if ($.fn.cookie("background") == "bg_cha") {
            b = "茶色"
        }
        if ($.fn.cookie("background") == "bg_yin") {
            b = "银色"
        }
        if ($.fn.cookie("background") == "bg_mi") {
            b = "米色"
        }
        $("#background2").val($.fn.cookie("background"));
        $("#background").val(b);
        $("body").addClass($.fn.cookie("background"));
        //$(".ydleft").addClass($.fn.cookie("background"));
        $(".yd_text2").addClass($.fn.cookie("background"))
    }
    if ($.fn.cookie("fontColor") != null && $.fn.cookie("fontColor") != "") {
        var a1 = "字色";
        if ($.fn.cookie("fontColor") == "z_hei") {
            a1 = "黑色"
        }
        if ($.fn.cookie("fontColor") == "z_red") {
            a1 = "红色"
        }
        if ($.fn.cookie("fontColor") == "z_lan") {
            a1 = "蓝色"
        }
        if ($.fn.cookie("fontColor") == "z_lv") {
            a1 = "绿色"
        }
        if ($.fn.cookie("fontColor") == "z_hui") {
            a1 = "灰色"
        }
        if ($.fn.cookie("fontColor") == "z_li") {
            a1 = "栗色"
        }
        if ($.fn.cookie("fontColor") == "z_wu") {
            a1 = "雾白"
        }
        if ($.fn.cookie("fontColor") == "z_zi") {
            a1 = "暗紫"
        }
        if ($.fn.cookie("fontColor") == "z_he") {
            a1 = "玫褐"
        }
        $("#fontColor2").val($.fn.cookie("fontColor"));
        $("#fontColor").val(a1);
        $(".yd_text2").addClass($.fn.cookie("fontColor"))
    }
    if ($.fn.cookie("fontFamily") != null && $.fn.cookie("fontFamily") != "") {
        var c = "字体";
        if ($.fn.cookie("fontFamily") == "fam_song") {
            c = "宋体"
        }
        if ($.fn.cookie("fontFamily") == "fam_hei") {
            c = "黑体"
        }
        if ($.fn.cookie("fontFamily") == "fam_kai") {
            c = "楷体"
        }
        if ($.fn.cookie("fontFamily") == "fam_qi") {
            c = "启体"
        }
        if ($.fn.cookie("fontFamily") == "fam_ya") {
            c = "雅黑"
        }
        $("#fontFamily2").val($.fn.cookie("fontFamily"));
        $("#fontFamily").val(c);
        $(".yd_text2").addClass($.fn.cookie("fontFamily"))
    }

}