$(document).ready(function(){
  $(document).scroll(function(){
    $(".tabitem.presentation h1").each(function(index){
      if($(this).offset().top > $(window).scrollTop()){
        if(index > 0){
          $(".sidemenu li:eq("+(index-1)+")").addClass("hover").siblings().removeClass("hover");
        }
        return false;
      }
    });
  });
});

