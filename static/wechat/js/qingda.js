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

	/*轮播*/
	if ($("#carousel").length > 0) {
		$('#carousel').slideBox({
			duration: 0.5, //滚动持续时间，单位：秒
			easing: 'linear', //swing,linear//滚动特效
			delay: 5, //滚动延迟时间，单位：秒
			hideClickBar: false, //不自动隐藏点选按键
			clickBarRadius: 10
		});
	}

});

var co_cover = $('.co_covers');
$(document).on("pageshow", "#pro_detail", function() {

	$.mobile.buttonMarkup.hoverDelay = "false";
	//alert(co_cover.height());
	//alert(co_cover.find('img').height());
	if (co_cover.length > 0) {

		$('#base_info').css('margin-top', co_cover.height());
		$(".progress .bar").css("width", $(".progressbar").attr("data") + '%');
	}

	//加载保利视频
	if ($("#plv_video").length > 0) {
		var player = polyvObject('#plv_video').videoPlayer({
			'width': '100%',
			'height': '200',
			'vid': $("#plv_video").attr('data')
		});
	} else {
		//alert('没有视频');
	}

});

$(".pro_detail #detailtabs").delegate(".ui-tabs-anchor", "click", function() {

	if ($(this).attr('id') == "ui-id-1") {
		$('#base_info').css('margin-top', co_cover.height());
		$(".progress .bar").css("width", $(".progressbar").attr("data") + '%');
		co_cover.css('display', 'block');
	} else {
		$('#base_info').css('margin-top', 0);
		co_cover.css('display', 'none');
	}
});

$(".follow").delegate(".follow-heart", "click", function() {
	if ($(this).hasClass('active')) {
		$(this).removeClass('active');
		$('#like_count').text(parseInt($('#like_count').text()) - 1);
		$.post("/w/like/", {
				'type': $(this).attr('type'),
				'id': $(this).attr('pid'),
				'focus': 'unlike'
			},
			function(data, status) {
				if(data.status == -1){
					window.location.href="/w/login/"; 
				}
			});
	} else {
		$(this).addClass('active');
		$('#like_count').text(parseInt($('#like_count').text()) + 1);
		$.post("/w/like/", {
				'type': $(this).attr('type'),
				'id': $(this).attr('pid'),
				'focus': 'like'
			},
			function(data, status) {
				if(data.status == -1){
					window.location.href="/w/login/"; 
				}
			});
	}
});