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


// register.html的js
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

	$("#passwordtest").blur(function(){
		$.ajax({
			url:'/c/passwordtest/?u_passwordtest='+$("#passwordtest").val()+'&u_password='+$("#password").val(),
			type:'get',
			dateType:'json',
			success:function(data){
				$("#u_pwdtest").text(data.msg);
				if (data.msg =="success")
					$("#u_pwdtest").hide();
				else
					$("#u_pwdtest").show();
			}

		});
	});







	$("#username").blur(function(){

		$.ajax({
			url:'/c/register1/?u_name='+$("#username").val(),
			type:'get',
			dateType:'json',
			success:function(data){
				$("#u_name").text(data.msg);
				if (data.msg =="success")
					$("#u_name").hide();
				else
					$("#u_name").show();
			}

		});
	});



	$("#telephone").blur(function(){

		$.ajax({
			url:'/c/register2/?u_tel='+$("#telephone").val(),
			type:'get',
			dateType:'json',
			success:function(data){
				$("#u_tel").text(data.msg);
				if (data.msg =="success")
					$("#u_tel").hide();
				else
					$("#u_tel").show();
			}

		});
	});



	$("#submit1").blur(function(){
		$.ajax({
			url:'/c/test/?u_telephone='+$("#telephone").val(),
			type:'get',
			dateType:'json',
			success:function(data){
				$("#test").text(data.msg);
				if (data.msg =="success")
					$("#test").hide();
				else
					$("#test").show();
			}

		});
	});



	$("#test1").blur(function(){
		$.ajax({
			url:'/c/test1/?u_test='+$("#test1").val()+'&u_telephone='+$("#telephone").val(),
			type:'get',
			dateType:'json',
			success:function(data){
				$("#test2").text(data.msg);
				if (data.msg =="success")
					$("#test2").hide();
				else
					$("#test2").show();
			}

		});
	});



	$("#submit").click(function(){

		if(($("#u_name").text()=="success") && ($("#u_pwd").text()=="success")&& ($("#u_pwdtest").text()=="success") && ($("#u_tel").text()=="success")&& ($("#test").text()=="success")&& ($("#test2").text()=="success"))
		{
			return true;
		}		
		else{
			alert("请按照提示认真填写信息");
			return false; 
		}
	});




// forget.html的js
	$("#username1").blur(function(){

		$.ajax({
			url:'/c/forget1/?u_name='+$("#username1").val(),
			type:'get',
			dateType:'json',
			success:function(data){
				$("#u_name1").text(data.msg);
				if (data.msg =="success")
					$("#u_name1").hide();
				else
					$("#u_name1").show();
			}

		});
	});


	$("#telephone1").blur(function(){
		$.ajax({
			url:'/c/forget3/?u_tel='+$("#telephone1").val()+'&username='+$("#username1").val(),
			type:'get',
			dateType:'json',
			success:function(data){
				$("#u_tel1").text(data.msg);
				if (data.msg =="success")
					$("#u_tel1").hide();
				else
					$("#u_tel1").show();
			}

		});
	});


	$("#button").blur(function(){
		$.ajax({
			url:'/c/forget4/?u_telephone='+$("#telephone1").val(),
			type:'get',
			dateType:'json',
			success:function(data){
				$("#button1").text(data.msg);
				if (data.msg =="success")
					$("#button1").hide();
				else
					$("#button1").show();
			}

		});
	});




	$("#tcod").blur(function(){
		$.ajax({
			url:'/c/forget5/?tcod='+$("#tcod").val()+'&telephone1='+$("#telephone1").val(),
			type:'get',
			dateType:'json',
			success:function(data){
				$("#tcod1").text(data.msg);
				if (data.msg =="success")
					$("#tcod1").hide();
				else
					$("#tcod1").show();
			}

		});
	});





	$("#alter").click(function(){

		if(($("#u_name1").text()=="success") &&($("#u_pwdtest").text()=="success") && ($("#u_tel1").text()=="success") && ($("#button1").text()=="success")&& ($("#u_pwd").text()=="success")&& ($("#tcod1").text()=="success"))
		{
			return true;
		}		
		else{
			alert("请按照提示认真填写信息");
			return false; 
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
