$(document).on("click","a[href^='panels/']",function(event){
	event.preventDefault();
	$hashed.doRefresh = false;
	window.location.hash = window.location.hash+"&"+Math.random(); // to let back button work
	
	$this = $(this);
	$panel = $("#panel");
	$panel.stop().show().fadeIn(300);
	$("#panelLoader").show();
	
	if($("#panel_"+encodeURIComponent($this.attr("href").replace(/./g,"_").replace(/\//g,"_slash-")).replace(/%/g,"_")).length>0){
		$("#panelContent, .preloadedPanel, #panelLoader").hide();
		$("#panel_"+encodeURIComponent($this.attr("href").replace(/./g,"_").replace(/\//g,"_slash-")).replace(/%/g,"_")).show();
		transformLinks();
		$events.sidepanelShow();
	}else{
		$.ajax($this.attr("href")).success(function(newContent,textStatus){	
			$("#panelContent, .preloadedPanel").hide()
			$("#panelLoader").fadeOut(200)
			$("#panelContent").html(newContent).show();
			transformLinks();
			$events.sidepanelShow();
		}).error(function(){hidePanel()});
	}
	
	$("#wrapper").css("display","none"); // hide wrapper to prevent ghost scrolling	
	setTimeout("$hashed.doRefresh = true;",100);
	return false;
});
hidePanel = function(){
	
	history.back();
}
/*Back button hack*/
$.plugin($hashChangeEnd,{
	panels:function(){
		if($hashed.doRefresh && $("#panel").css("display") != "none"){
			$("#wrapper").css("display","block");
			$("#panel").animate({right:-$("#panel").width()-20},500,"easeOutCubic",function(){
				$(this).hide();
			});
			$events.sidepanelHide();
		}
	}
});