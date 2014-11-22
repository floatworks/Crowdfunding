// JavaScript Document
$(document).ready(function(){

	//加载保利视频
	if($("#plv_video").length>0){
		var player = polyvObject('#plv_video').videoPlayer({
		'width':'600',
		'height':'337',
		'vid' : $("#plv_video").attr('data')
		});
	}else{
		//alert('没有视频');
	}
})