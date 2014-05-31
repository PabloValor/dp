$(document).on("click","a[href^='panels/']",function(event){
	event.preventDefault();
	$this = $(this);
	$panel = $("#panel");
	
	$panel.stop().show().animate({right:0},500, "easeOutCubic");
	$("#panelLoader").show()
	
	if($("#panel_"+encodeURIComponent($this.attr("href").replace(/./g,"_").replace(/\//g,"_slash-")).replace(/%/g,"_")).length>0){
		$("#panelContent, .preloadedPanel, #panelLoader").hide();
		$("#panel_"+encodeURIComponent($this.attr("href").replace(/./g,"_").replace(/\//g,"_slash-")).replace(/%/g,"_")).fadeIn(300);
		if(panelDim){
			$("#catchScroll").animate({opacity:panelDim},500).css("z-index",49);
		};
		if(!panelGroupScrolling){
			scrolling=true;
		}
		transformLinks();
		$events.sidepanelShow();
	}else{
		$.ajax($this.attr("href")).success(function(newContent,textStatus){	
			$("#panelContent, .preloadedPanel").hide()
			$("#panelLoader").fadeOut(200)
			$("#panelContent").html(newContent).fadeIn(300);
			if(panelDim){
				$("#catchScroll").animate({opacity:panelDim},500).css("z-index",49);
			};
			if(!panelGroupScrolling){
				scrolling=true;
			}
			transformLinks();
			$events.sidepanelShow();
		});
	}	
	if(hidePanelOnClick){
		$(document).bind("click.hidepanel",function(){
			hidePanel();
			$(document).unbind("click.hidepanel");
		});
		 $panel.click(function(event){
	    	 event.stopPropagation();
	 	});
	}
	
	return false;
});
hidePanel = function(){
	$("#panel").animate({right:-$("#panel").width()-20},500,"easeOutCubic",function(){
		$(this).hide();
		if(!panelGroupScrolling){
			scrolling=false;
		}
	});
	$("#catchScroll").animate({opacity:0},500).css("z-index",-1);
	$events.sidepanelHide();
}