$(document).on("pageinit", "#index", function() {
	/*进度条*/
	if ($(".progressbar").length > 0) {
		$(".progressbar").each(function() {
			var pb = $(this).attr("data");
			if (pb <= 50) {
				$(this).addClass("less");

			} else {
				$(this).addClass("more");
			}
			$(this).find(".num").text(pb + '%');
			$(this).find(".bar").css("width", pb + '%');
		})
	}

	if ($("#carousel").length > 0) {
		$('#carousel').slideBox({
			duration: 0.5, //滚动持续时间，单位：秒
			easing: 'linear', //swing,linear//滚动特效
			delay: 5, //滚动延迟时间，单位：秒
			hideClickBar: false, //不自动隐藏点选按键
			clickBarRadius: 10
		});
	}
	/*轮播*/



});