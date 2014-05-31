/*flip tile 0.1 */
if($.browser.name=="msie"){	
	$(document).on("mouseenter",".tileFlipText",function(){
		$(this).find(".flipFront, .tileLabelWrapper").stop().fadeOut(500);
	}).on("mouseleave",".tileFlipText",function(){
		$(this).find(".flipFront, .tileLabelWrapper").stop().fadeIn(500);
	})
}else{
	$(document).ready(function(){
		$(".tileFlipText").addClass("support3D");
	});
	$(document).on("mouseenter",".tileFlipText",function(){
		$(this).find(".flipFront, .tileLabelWrapper").stop().delay(300).animate({opacity:0},0)
	}).on("mouseleave",".tileFlipText",function(){
		$(this).find(".flipFront, .tileLabelWrapper").stop().animate({opacity:1},0);
	})	
}