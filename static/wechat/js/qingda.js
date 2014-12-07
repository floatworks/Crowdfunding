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
	$('.pro_detail .ui-tabs').css('padding-top',$('.relative > .ui-grid-b').height()+$('.relative > .ui-grid-solo').height());
	if (co_cover.length > 0) {
		//$('#base_info').css('margin-top', co_cover.height());
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
		min_price = $(this).attr('min');
		if (price == null || price == '') {
			$("#input-money").val('');
			popDialog('#investDialog','认购金额不能为空');
			return;
		}else if(parseFloat(price) < parseFloat(min_price)){
			popDialog('#investDialog','认购金额不能少于认购起点');
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
				}else if(data.status == 1){
					popDialog('#investDialog','认购成功');
					$('#invest_count').text(parseInt($('#invest_count').text())+1);
				}
			});
		$("#input-money").val('');
	});

});

$(document).on("pageinit", "#feedback", function() {
	$('#feedback_btn').click(function() {
		mail = $("#fb_email").val().trim();
		content = $("#fb_textarea").val().trim();
		if(!mail.match($.regexpCommon('email'))){
			popDialog('#feedbackDialog','邮箱地址不合法');
			return false;
		}else if(content == null || content == ''){
			popDialog('#feedbackDialog','反馈内容不能为空');
			return false;
		}

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

$(document).on("pageshow", "#login", function() {
	var status = $.getUrlParam('s');
	if(status == 'reg#' || status == 'reg'){
		popDialog('#loginDialog','注册成功，请登录');
	}else if(status == 'err' || status == 'err#'){
		popDialog('#loginDialog','用户名或密码错误');
	}
});

$(document).on("pageshow", "#reg", function() {
	var status = $.getUrlParam('s');
	if(status == 2){
		popDialog('#popupDialog','用户名已存在');
	}else if(status == 3){
		popDialog('#popupDialog','该手机号码已被注册');
	}else if(status == 4){
		popDialog('#popupDialog','验证码错误');
	}
});
//注册校验
function checkReg(){
	u_name = $("#u_name").val().trim();
	u_pwd = $("#u_pwd").val().trim();
	cpw = $("#cpw").val().trim();
	tel = $("#u_tel").val().trim();
	code = $("#code").val().trim();
	if(!u_name.match($.regexpCommon('username'))){
		popDialog('#popupDialog','请输入6至20位用户名');
		return false;
	}else if(!u_pwd.match($.regexpCommon('pwd'))){
		popDialog('#popupDialog','请输入6至16位密码');
		return false;
	}else if(u_pwd != cpw){
		popDialog('#popupDialog','两次密码不同');
		return false;
	}else if(!tel.match($.regexpCommon('phoneNumberZN'))){
		popDialog('#popupDialog','手机号码格式不正确');
		return false;
	}else if(!code.match($.regexpCommon('code'))){
		popDialog('#popupDialog','验证码为6位数字');
		return false;
	}else if($('#agreement').attr('data-cacheval') != 'false'){
		popDialog('#popupDialog','请阅读并确认用户服务协议');
		return false;
	}
	return true;
}

//Dialog弹出
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