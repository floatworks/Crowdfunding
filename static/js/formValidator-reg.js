$(document).ready(function(){
	$.formValidator.initConfig({formID:"client_form",theme:"Default",submitOnce:true,
		onError:function(msg,obj,errorlist){
			$("#errorlist").empty();
			$.map(errorlist,function(msg){
				$("#errorlist").append("<li>" + msg + "</li>")
			});
			alert(msg);
		},
		ajaxPrompt : '有数据正在异步验证，请稍等...'
	});
	$("#username").blur(function(){
		var v=$("#username").val();
		var t=/^[a-zA-Z0-9]{1}[0-9a-zA-Z]{1,}$/;
		if(!t.test(v)){
			$("#u_name").text("用户名为6至15位数字或字母");
			$("#u_name").show();
		}
		else if(v.length <6){
			$("#u_name").text("用户名长度不能小于6");
			$("#u_name").show();
		}
		else if(v.length >15){
			$("#u_name").text("用户名长度不能大于15");
			$("#u_name").show();
		}
		else{
			$("#u_name").text("success");
			$("#u_name").hide();
		}
	});


	$("#password").blur(function(){
		var v=$("#password").val();
		var t=/^[A-Za-z].*[0-9].*|[0-9].*[A-Za-z].*$/;
		if(!t.test(v)){
			$("#u_pwd").text("必须同时包含数字和字母");
			$("#u_pwd").show();
		}
		else if(v.length <6){
			$("#u_pwd").text("密码长度不能小于6");
			$("#u_pwd").show();
		}
		else if(v.length >15){
			$("#u_pwd").text("密码长度不能大于15");
			$("#u_pwd").show();
		}
		else{
			$("#u_pwd").text("success");
			$("#u_pwd").hide();
		}
	});

	$("#telephone").blur(function(){
		var v=$("#telephone").val();
		var t=/^13[0-9]{9}|15[012356789][0-9]{8}|18[0256789][0-9]{8}|147[0-9]{8}$/;
		if(!t.test(v)){
			$("#u_tel").text("你输入的电话号码无效");
			$("#u_tel").show();
		}
		else if(v.length!= 11){
			$("#u_tel").text("密码长度应为11位");
			$("#u_tel").show();
		}		
		else{
			$("#u_tel").text("success");
			$("#u_tel").hide();
		}
	});


	$("#clt_mail").formValidator({onFocus:"请务必填写有效的电邮地址",onCorrect:"&nbsp"})
				  .inputValidator({min:1,onError:"电邮地址不能为空"})
				  .regexValidator({regExp:"email",dataType:"enum",onError:"email格式不正确"})
				  .ajaxValidator({
				  	type:'get',
				  	dataType:'json',
				  	//async:true,
				  	url:'/t/reg_validator/',
				  	success:function(data){
				  		if(data.msg.indexOf('yes')>=0)
				  			return true;
				  		return false;
				  	},
				  	buttons:$("#submit"),
				  	error: function(jqXHR, textStatus, errorThrown){
				  		alert("服务器忙，请重试"+errorThrown);
				  	},
					onError: "该邮箱已被注册",
					onWait: "正在校验邮箱，请稍候..."
				  }).defaultPassed();
	$("#clt_pwd").formValidator({onFocus:"6至15位数字或字母",onCorrect:"&nbsp"})
				 .inputValidator({min:6,max:15,empty:{leftEmpty:false,rightEmpty:false,emptyError:"密码两边不能有空符号"},onError:"密码长度不合法"})
				 .regexValidator({regExp:["username"],dataType:"enum",onError:"只能包含数字或字母"});
	$("#clt_pwd_a").formValidator({onFocus:"6至15位数字或字母",onCorrect:"&nbsp"})
				   .inputValidator({min:6,max:15,empty:{leftEmpty:false,rightEmpty:false,emptyError:"密码两边不能有空符号"},onError:"密码长度不合法"})
				   .compareValidator({desID:"clt_pwd",operateor:"=",onError:"2次密码不一致,请确认"})
				   .regexValidator({regExp:["username"],dataType:"enum",onError:"只能包含数字或字母"});
	$("#clt_name").formValidator({onCorrect:"&nbsp"})
				  .inputValidator({min:1,onError:"称呼不能为空"});
	$("#clt_tel").formValidator({onFocus:"固话或手机号码",onCorrect:"&nbsp"})
				 .inputValidator({min:1,onError:"联系方式不能为空"})
				 .regexValidator({regExp:["tel","mobile"],dataType:"enum",onError:"手机或电话格式不正确"});
	$("#clt_company").formValidator({onCorrect:"&nbsp"})
					 .inputValidator({min:1,onError:"公司名称不能为空"});
	$("#confirm").inputValidator({min:1,onError:"公司名称不能为空"});		 
})