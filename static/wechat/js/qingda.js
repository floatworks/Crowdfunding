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


});

$(document).on("pageinit", "#pro_detail", function() {

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

	$('#invest_button').click(function() {
		price = $("#input-money").val().trim();
		type = $(this).attr('type');
		id = $(this).attr('pid');
		if (price == null || price == '') {
			$("#input-money").val('');
			return;
		}
		$.post("/w/invest/", {
				'type': type,
				'id': id,
				'price': price
			},
			function(data, status) {
				if (data.status == -1) {
					window.location.href = "/w/login/";
				}
			});
		$("#input-money").val('');
	});

});

$(document).on("pageinit", "#feedback", function() {
	$('#feedback_btn').click(function() {
		mail = $("#fb_email").val().trim();
		content = $("#fb_textarea").val().trim();
		$.post("/w/feedback/", {
				'mail': mail,
				'content': content
			},
			function(data, status) {
				if (data.status == -1) {
					window.location.href = "/w/login/";
				} else if (data.status == 1) {
					window.location.href = "/w/setting/";
				}
			});
	});
});

$(document).on("pageinit", "#reg", function() {
	$('#getCode').click(function() {
		tel = $("#u_tel").val().trim();
		if (!tel.match($.regexpCommon('phoneNumberZN'))) {
			popDialog('#popupDialog','手机号码格式不正确');
			return;
		}
		$.get("/app/code/", {
				'type': 'reg',
				'u_tel': tel
			},
			function(data, status) {
				if(data.status == 2){
					popDialog('#popupDialog','该手机号码已经被注册');
				}else if (data.status == 1) {
					popDialog('#popupDialog','验证码发送成功，请注意查收');
				}
			});
	});
});

function popDialog(dialogID,text){
	$(dialogID+" h3").text(text);
	$(dialogID).popup('open');  
}

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
				if (data.status == -1) {
					window.location.href = "/w/login/";
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
				if (data.status == -1) {
					window.location.href = "/w/login/";
				}
			});
	}
});


$("#feedback #fb_textarea").keyup(function() {
	(($(this).val().length) >= 80) ? ($("#ta_num").text('80/80')) : ($("#ta_num").text($(this).val().length + '/80'));

})