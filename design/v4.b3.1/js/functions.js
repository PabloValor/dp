/* METRO UI TEMPLATE 
/* Copyright 2012 Thomas Verelst, http://metro-webdesign.info*/


/*Functions that will be used everywhere, mainly in main.js */


scrolling = false;
scaleSpacing = scale+spacing;

$page.current = "";
$page.layout = "full";
$page.smallWidth = -1;

$group.count = $group.titles.length;
$group.current = -1;

$arrows.rightArray = [];
mostRight = 0;
mostDown = 0;
tileContainer = "";
zoomScale = 1;

$hashed.parts = [];
$hashed.get = [];
$hashed.doRefresh = true;

submenu = [];

$group.spacing = $group.spacingFull.slice(); // clone arrays

/*Replace spaces by hyphens. ( - )  for TEXT to URL*/
String.prototype.stripSpaces = function(){ return this.replace(/\s/g,"-")}
/*Replace hyphens by spaces, for URL to TEXT */
String.prototype.addSpaces = function(){ return this.replace(/-/g," ")}
/*Case insensitive array search and returns the index of that search in the array */
inArrayNCindex = function(val,array){var i=array.length;val=chars(val.toLowerCase());while (i--){if(chars(array[i].toLowerCase())==val){return i;}}return -1;}
inArrayNCkey = function(val,array){val=chars(val.toLowerCase());for(var key in array){if(chars(array[key].toLowerCase())==val){return key;}}return -1;}
/* Returns the case sensitive index after a case insensitive index search */
strRepeat = function(cnt,char){var a = [],x = cnt + 1;while (x--) { a[x] = '';}return a.join(char);}

/*PHP strtr equivalent*/
chars = function(r){
	r = r.replace(new RegExp("[àáâãäåæąĄ]", 'g'),"a");
	r = r.replace(new RegExp("[çćĆ]", 'g'),"c");
	r = r.replace(new RegExp("[èéêëęĘ]", 'g'),"e");
	r = r.replace(new RegExp("[ìíîï]", 'g'),"i");
	r = r.replace(new RegExp("[ñńŃ]", 'g'),"n");     
	r = r.replace(new RegExp("[òóôõöðøóÓ]", 'g'),"o");
	r = r.replace(new RegExp("[œ]", 'g'),"oe");
	r = r.replace(new RegExp("[ùúûü]", 'g'),"u");
	r = r.replace(new RegExp("[ýÿ]", 'g'),"y");
	r = r.replace(new RegExp("[šśŚ]", 'g'),"s");
	r = r.replace(new RegExp("[žżŻźŹ]", 'g'),"z");
	r = r.replace(new RegExp("[Þ]", 'g'),"b");
	r = r.replace(new RegExp("[ß]", 'g'),"ss");
	r = r.replace(new RegExp("[ƒ]", 'g'),"f");
	r = r.replace(new RegExp("[łŁ]", 'g'),"l");
	return r;
};

/* Init the tile-pages move functions */
$.extend($group, {	
	goTo: function(n){
		if($page.current != "home"){
			window.location.hash = "&"+$group.titles[n].toLowerCase().stripSpaces();
			$show.prepareTiles();
		}
		$tileContainer = $("#tileContainer");
		scrolling = true;
		if(n<0){n=0};
		$group.current = n;	
		
		$tileContainer.children(".navArrows").hide();
		if($page.layout=="column" || $group.direction == "vertical") {
			$("html, body").animate({"scrollTop":$("#groupTitle"+n).offset().top-!scrollHeader*$("header").height()-10},scrollSpeed,function(){
				document.title = siteTitle+" | "+$group.titles[$group.current];
				if (history.pushState) {
					window.history.replaceState("", "", "#&"+chars($group.titles[$group.current].toLowerCase()).stripSpaces());
				}
				setTimeout("scrolling = false",100);
				$arrows.place(300);
				$events.tileGroupChangeEnd();	
			});	
		}else{
			$("html, body").animate({"scrollLeft":getMarginLeft(n)*zoomScale},scrollSpeed,function(){
				document.title = siteTitle+" | "+$group.titles[$group.current];
				if (history.pushState) {
					window.history.replaceState("", "", "#&"+chars($group.titles[$group.current].toLowerCase()).stripSpaces());
				}
				setTimeout("scrolling = false",100);
				$arrows.place(300);
				$events.tileGroupChangeEnd();	
			});
		}
	
		$mainNav.setActive();
		setTileOpacity();
		
		scrollBg();	
		$events.tileGroupChangeBegin();	
	},
	goLeft: function(){
		if($group.current>0){
			$group.goTo($group.current-1);
		}else{
			$group.bounce(-1);
		}
	},
	goRight: function(){
		if($group.current+1 < $group.count){
			$group.goTo($group.current+1);
		}else{
			$group.bounce(1);
		}
	},
	bounce: function(s){ //gives a bounce effect when there are no pages anymore, s = side: -1 = left, 1 = right
		if(!scrolling){	
			scrolling = true;
			var t;
			if(s>0){t = "-=40"}else{t="+=40";}
			$('#tileContainer').animate({'margin-left': t}, 150).animate({'margin-left':  0}, 150,function(){
				scrolling = false	
			});	
		}
	}
});

/*Calculates the margin left for tiles/scrolling */
getMarginLeft=function(l){
	var s=0;
	for(i=0;i<l;i++){
		if($group.spacing.length>i){ // if in array (to prevent errors);
			s+=$group.spacing[i];
		}else{
			s+=$group.spacing[$group.spacing.length-1]; // add last defined groupSpacing
		}
	}
	return s*scaleSpacing;
}

/* Place the arrows on the right place*/
$.extend($arrows,{
	place:function(speed){
		if($group.direction=="horizontal"){
			if($page.layout == "full"){
				$("#tileContainer").children(".navArrows").hide();
				if($group.current!=0){
					$("#arrowLeft").css('margin-left',getMarginLeft($group.current)-40).fadeTo(speed,0.5);
				}
				if($group.current!=($group.count-1)){		
					$("#arrowRight").css('margin-left',$arrows.rightArray[$group.current]+12).fadeTo(speed,0.5);
				}
			}else if($page.layout == "small"){
				$("#tileContainer").children(".navArrows").hide();
				if($group.current!=0){
					$("#arrowLeft").css('margin-left',getMarginLeft($group.current)-40).fadeTo(speed,0.5);
				}
				if($group.current!=($group.count-1)){
					$("#arrowRight").css('margin-left',getMarginLeft($group.current)+scaleSpacing*2+scale+12).fadeTo(speed,0.5);
				}	
			}else{
				$("#tileContainer").children(".navArrows").hide();
			}
			$events.arrowsPlaced();	
		}
	}
});
/* Hover FX for nav arrows*/
$(document).ready(function(){
	$(".navArrows").bind("mouseover",function(){
		if(!scrolling){
			$(this).stop(false,true).fadeTo(300,1);
		}
	}).bind("mouseleave",function(){
		if(!scrolling){
			$(this).stop(false,true).fadeTo(300,0.5);
		}
	})
});

/* Scrolls background, if needed */
scrollBg = function(){
	if($page.layout != "column" && device=="desktop" && $group.direction == "horizontal"){
		if(bgMaxScroll!=0){
			var t = -$group.current*bgScroll;
			if(t>0){t=0};
			if($.browser.name == "msie" && $.browser.version<10){ // IE9 or lower
				$('#bgImage').stop().animate({marginLeft:t},bgScrollSpeed);
			}else{ // if IE10 or other browser
				$('#bgImage').css("margin-left",t);	
			}
		}
		$events.bgScroll();
	}
}

/* Set width so we can scroll to last tilegroup */
fixScrolling = function(){
	var t;
	if($page.layout != "column" && $group.direction == "horizontal"){
		if($("#groupTitle"+($group.titles.length-1)).length>0){
			t = parseInt(($("#groupTitle"+($group.titles.length-1)).css("margin-left")).replace("px",""))/zoomScale+25;
			t +=$("#headerCenter").width()+($(window).width()-$("#headerCenter").width())/2;
		}
	}else{
		t=scaleSpacing+scale+10;	
	}
	$events.fixScrolling();
	$("#tileContainer").width(t).height(mostDown+($group.direction=="vertical")*$group.spacingFull.pop()*scaleSpacing);
}

recalcScrolling = function(){
	mostDown = 0;
	$("#tileContainer").children(".tile").each(function(){
		var thisRight = parseInt($(this).css("margin-left"))+$(this).width(); // GLOBAL
		if(thisRight>mostRight){
			mostRight=thisRight;
		}
		var thisDown= parseInt($(this).css("margin-top"))+$(this).height();
		if(thisDown>mostDown){
			mostDown=thisDown;
		}		
	})
	$events.recalcScrolling();
}

/* To create subnav */
$subNav={
	make: function(){/* Generates the subnav- menu, makes sub-Navigation items */
		$("#subNavWrapper").children("#subNav").remove();
		$("#subNavTemp").children().prependTo("#subNavWrapper");
		$("#subNavTemp").remove();
		$("#subNav").children("a").each(function(){
			$(this).attr("href",$(this).attr("href").replace("?p=","#!/"));
		});	
		$subNav.setActive();
		$events.subNavMake();
	},
	/* highlights current sub-navigation-item */
	setActive: function(){
		var $nav = $("#subNav");
		$nav.children("a").removeClass("subNavItemActive");
		$nav.children('[href$="'+$hashed.parts[0]+'"]').addClass("subNavItemActive");
		$events.subNavActive();
	}
}

/* Makes main (top) nav */
$mainNav={
	init: function(){
		$("nav").on("click","a",function(){
			if(typeof $(this).attr("rel")!=="undefined"){
                 $group.goTo(parseInt($(this).attr("rel").replace("group","")));
            }
            if(typeof $(this).attr("id")!=="undefined"){
                 $group.goTo(parseInt($(this).attr("id").replace("group","")));
            }
		});
		$events.mainNavInit();
	},
	setActive: function(){
		var $nav = $("nav")
		$nav.children("a").removeClass("navActive");
		$nav.children("[rel='group"+$group.current+"']").addClass("navActive");
		$nav.children("#group"+$group.current).addClass("navActive");
		$events.mainNavActive();
	},
	set:function(w){/* Used to manually select the highlighted menu */
		var $nav = $("nav")
		w = $.trim(w.toLowerCase());
		$nav.children("a").removeClass("navActive");
		$nav.children("a").each(function(){
			if($.trim($(this).text().toLowerCase()) == w.toLowerCase()){
				$(this).addClass("navActive");
			}
		});
		$events.mainNavSet();
	}
}

/*For smaller column mainnav */
$(document).on("click","#navTitle",function(){
	if($("nav>a").css("display") == "none"){
		$("nav>a").css("display","block");
	}else{
		$("nav>a").css("display","none");
	}
});

/* Creates a nice link according to the required page */
makeLink = function(lp){/* To make valid links */
	if(lp.substr(0,9) == 'external:' || lp.substr(0,9) == 'gotolink:'){
		return lp.substr(9);
	}
	if(lp==""){
		return '';
	}
	if(lp.substr(0,7) == "http://" ||
	   lp.substr(0,8) == "https://" ||
	   lp.substr(0,1) == "/" ||
	   lp.substr(0,1) == "#" ||
	   lp[lp.length-1] == "/")
	{
		return lp;
	}
	$events.makeLink();
	if(typeof pageTitles[lp] == "undefined" ){
		return "#!/url="+chars(lp.toLowerCase().stripSpaces());
	}else{
		return "#!/"+chars(pageTitles[lp].toLowerCase().stripSpaces());			
	}
}

/* For menu / tile links, generates the link + href + target attribute if needed */
makeLinkHref = function(lp){/* To make valid links */
	var t = '';
	if(lp.substr(0,9) == 'external:'){
		t=" target='_blank' ";
		lp = lp.substr(9);
	}
	$events.makeLinkHref();
	if(lp == ""){
		return "";
	}
	return t+" href='"+makeLink(lp)+"' ";	
}

/* Will be called on page load to transform urls to nice urls */
transformLinks = function(){
	$("a[rel=metro-link]").each(function(){
		$(this).attr("href",$(this).attr("href").replace("?p=","#!/"));
	});
	$events.transformLinks();
}

/*Fired when clicked on any link*/
$(document).on("click","a",function(){	
	if(this.href==window.location.href){ // if we're already on the page the user wants to go
		$(window).hashchange(); // just refresh page
	};
});