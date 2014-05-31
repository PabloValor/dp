if($.browser.name=="msie"){	
	$(document).on("mouseenter",".tileFlip",function(){
		$(this).find(".flipFront, .tileLabelWrapper").stop().fadeOut(500);
	}).on("mouseleave",".tileFlip",function(){
		$(this).find(".flipFront, .tileLabelWrapper").stop().fadeIn(500);
	})
}else{
	$(document).ready(function(){
		$(".tileFlip").addClass("support3D");
	});
	$(document).on("mouseenter",".tileFlip",function(){
		$(this).find(".flipFront, .tileLabelWrapper").stop().delay(300).animate({opacity:0},0)
	}).on("mouseleave",".tileFlip",function(){
		$(this).find(".flipFront, .tileLabelWrapper").stop().animate({opacity:1},0);
	})
	
}