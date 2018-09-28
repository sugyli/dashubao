$(function () {
	var zan_status = showzanview()
	if(!zan_status){
		var data = "bookid=" + config.bookid+ '&isview=1'
		$.ajax({
			url: config.adduserzan,
			type: "post",
			data: data,
			async: true,
			beforeSend:function(xhr, settings){
				xhr.setRequestHeader("X-CSRFToken", config.csrf_token);
			},
			success: function (data) {
				showzanview()
			},

		});

	}
	//点 赞
	$("#zan").on("click", function() {
		var _self = $(this);
		var data = "bookid=" + config.bookid
		$.ajax({
			url: config.adduserzan,
			type: "post",
			data: data,
			async: true,
			beforeSend:function(xhr, settings){
				layer.open({type: 2,shadeClose: true});
				xhr.setRequestHeader("X-CSRFToken", config.csrf_token);
			},
			success: function (data) {
				layer.closeAll();
				showzanview()
				if(data.msg){
					showmsg(data.msg)
				}

			},
			error: function(){
				layer.closeAll();
				showmsg('请求失败')
			}
		});

	});
		//Side Spen
	$(".sidespen .close-icon").on("click", function() {
		$(this).parents(".sidespen").remove();
	});

	//收藏
	$("#shuqian").on("click", function() {
		var _self = $(this);
		var data = "bookid=" + config.bookid +"&chapterid=" + config.chapterid

		$.ajax({
			url: config.adduserfav,
			type: "post",
			data: data,
			async: true,
			beforeSend:function(xhr, settings){
				layer.open({type: 2,shadeClose: true});
				xhr.setRequestHeader("X-CSRFToken", config.csrf_token);
			},
			success: function (data) {
				layer.closeAll();
				if(data.bookid){
					showmsg(data.bookid)
				}else if(data.chapterid){
					showmsg(data.chapterid)
				}else if(data.msg){
					showmsg(data.msg)
				}

			},
			error: function(){
				layer.closeAll();
				showmsg('请求失败')
			}
		});

	});

    $(".article-set .a-minus").on("click", function() {
		font.descrease();
	});
    $(".article-set .a-plus").on("click", function() {
		font.increase();
	});
    $(".article-set .pattern").on("click", function() {
		if(isNight) {
			font.day();
		}else{
			font.night();
		}
	});




    /*
	$(".article-set .correct").on("click", function () {
	    $("body").append("<div class=\"mask-bg modal-mask-bg\"></div>");
	    if ($(".correct-md").length == 0) {
	        var msgSubmit = '<div class="modal correct-md">';
	        msgSubmit += '<div class="modal-hd"><h3>纠错</h3><a href="javascript:void(0);" class="icon close-icon"></a></div>';
	        msgSubmit += '<div class="modal-con"><div class="clearfix labels"><a href="javascript:void(0);" class="active">章节内容错误</a><a href="javascript:void(0);">错别字较多</a><a href="javascript:void(0);">低俗情色</a></div>';
	        msgSubmit += '<div class="text-box"><textarea placeholder="不能超过500个字" rows="3" class="form-text correct-text"></textarea></div></div>';
	        msgSubmit += '<div class="modal-ft"><a href="javascript:void(0)" class="btn cancel-btn">取消</a><a href="javascript:void(0)" class="btn confirm-btn error">提交</a></div>';
	        msgSubmit += '</div>';
	        $("body").append(msgSubmit);
	    }
		setTimeout(function(){
			$(".correct-md").addClass("show-md").css({transform:"translateY(0)"});
		},50);
	});


	$("body").on("click", ".modal .error", function () {
	    var url = window.location.href;
	    var data = "message=" + encodeURI($(".labels .active").text()) +' '+ encodeURI($(".correct-text").val() + '_' + url)
		layer.open({type: 2,shadeClose: true});
	    $.ajax({
	        url: config.adduserask,
	        type: "post",
	        data: data,
			async: true,
			beforeSend:function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", config.csrf_token);
            },
	        success: function (data) {
	        	layer.closeAll();
	        	if(data.message){
	        		showmsg(data.message)

                }else if(data.status == "success"){
                    showmsg('提交成功')
                }else if(data.msg){

	        		showmsg(data.msg)
				}

	        },
			error: function(){
	        	layer.closeAll();
	        	showmsg('请求失败')
            }
	    });
	    $(".modal .close-icon").click();

	});

	$("body").on("click", ".correct-md .labels a", function() {
		$(this).siblings("a").removeClass("active");
		$(this).addClass("active");
	});
	$("body").on("click", ".modal-mask-bg", function() {
	    $(".show-md").css({transform:"translateY(100%)"}).removeClass("show-md");
	    $(".modal-mask-bg").remove();
	});
	$("body").on("click", ".modal .cancel-btn, .modal .close-icon", function () {
	    $(this).parents(".modal").css({transform:"translateY(100%)"}).removeClass("show-md");
	    $(".modal-mask-bg").remove();
	});
	*/




});


function showzanview(){
	var zan = Number($.fn.cookie("zan"))
	if(zan == 1){
		$("#zan").html("<span class=\"circle\"><i class=\"icon quxiaozan-icon\"></i></span>取消点赞");
		return true
	}else if (zan == 2) {
        $("#zan").html("<span class=\"circle\"><i class=\"icon dianzan-icon\"></i></span>给作者点赞");
        return true
    }else {
		return false
	}

}

var isNight = $.fn.cookie("LightChange");
var chapterView = $(".article-con");
var pageContent = $(".article-bd"), saveFont = $.fn.cookie("CurrentFont"), currentFont = 0;
var font = function () {
	var sizes = ["font-normal", "font-large", "font-xlarge", "font-xxlarge", "font-xxxlarge"],
		level = sizes.length;
		return {
			set: function (c) {
				//console.log(c);
				//console.log(sizes[c]);
				pageContent.removeClass().addClass("article-bd" + " " + sizes[c]);
				currentFont = c;
				$.fn.cookie("CurrentFont", c, { expires: 3600, path: "/" });
				$.fn.cookie("currentFontString", sizes[c], { expires: 3600, path: "/" });
			},
			increase: function () {
				if(currentFont < level - 1) {
					this.set(currentFont + 1);
				}
			},
			descrease: function () {
				if(currentFont > 0) {
					this.set(currentFont - 1);
				}
			},
			night: function () {
				isNight = true;
				chapterView.addClass("turnoff");
				$(".moon-icon").removeClass().addClass("icon sun-icon");
				$.fn.cookie("LightChange", true, { expires: 3600, path: "/" });
			},
			day: function () {
				isNight = false;
				chapterView.removeClass("turnoff");
				$(".sun-icon").removeClass().addClass("icon moon-icon");
				$.fn.cookie("LightChange", false, { expires: -1, path: "/" });
			},



		}


}();
if(typeof saveFont !== "undefined") {
	if(saveFont == null) {
		saveFont = 0;
	}

	font.set(saveFont * 1);

}
if(isNight) {
	font.night();
}

