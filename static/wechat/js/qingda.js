$(document).ready(function(){
	/*进度条相关*/
	$(".progressbar").each(function(){
		var pb = $(this).attr("data");
	if(pb <= 50){
		$(this).addClass("less");
		
	}else{
		$(this).addClass("more");
	}
	$(this).find(".num").text(pb+'%');
	$(this).find(".bar").css("width",pb+'%');
	})
	
});