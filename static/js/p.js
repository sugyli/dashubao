function showmsg(msg){
	layer.open({
		content: msg
		,btn: '我知道了'
		,shadeClose: true
	});
}

//Set Cookie
$.fn.cookie = function (name, value, options) {
	if(typeof value != 'undefined') { // name and value given, set cookie
		options = options || {};
		if(value === null) {
			value = '';
			options.expires = -1;
		}
		var expires = '';
		if(options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
			var date;
			if(typeof options.expires == 'number') {
				date = new Date();
				date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
			}else{
				date = options.expires;
			}
			expires = '; expires=' + date.toGMTString(); // use expires attribute, max-age is not supported by IE
		}
		var path = options.path ? '; path=' + options.path : '';
		var domain = options.domain ? '; domain=' + options.domain : '';
		var secure = options.secure ? '; secure' : '';
		document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure, ';'].join('');
	}else{ // only name given, get cookie
		var cookieValue = null;
		if(document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = $.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if(cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
};
// 重写js array.push 避免添加重复元素
Array.prototype.oldUnshift=Array.prototype.unshift;
Array.prototype.pushSetObj=function(obj){
								var whetherRepeat=false;
									//alert(obj.name);
								for(var i=0;i<this.length;i++){
									if(this[i].bookid==obj.bookid){
										this.splice(i,1);
										this.unshift(obj);
										whetherRepeat=true;
										break;
									}
								}
								if(!whetherRepeat){
									this.oldUnshift(obj);
								}
								return whetherRepeat;
							}

function toVaild(){
	var val = $.trim(document.getElementById("q").value);
	if (!val){
		return false;

	}
}

$(document).ready(function(){

	//收藏
	$(".addshuqian").on("click", function() {
		var _self = $(this);
		var data = "bookid=" + bookid +"&chapterid=" + chapterid
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

	//点赞
	$(".zan").on("click", function() {
		var _self = $(this);
		var data = "bookid=" + bookid
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
				if(data.msg){
					showmsg(data.msg)
				}else {
					showmsg('投票失败')
				}

			},
			error: function(){
				layer.closeAll();
				showmsg('请求失败')
			}
		});

	});

});