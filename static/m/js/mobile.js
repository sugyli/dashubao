$(function () {

		//Side Spen
	$(".sidespen .close-icon").on("click", function() {
		$(this).parents(".sidespen").remove();
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

});


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

