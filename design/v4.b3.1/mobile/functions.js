/* METRO UI TEMPLATE 
/* Copyright 2012 Thomas Verelst, http://metro-webdesign.info*/


/*Functions that will be used everywhere, mainly in main.js */

scrolling = false;
scaleSpacing = scale+spacing;

$page.current = "";
$page.layout = "full";

$group.count = $group.titles.length;
$group.current = -1;

mostRight = 0;
mostDown = 0;
tileContainer = "";

$hashed.parts = [];
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
		$("html, body").animate({"scrollTop":$("#groupTitle"+n).offset().top},scrollSpeed,function(){
			document.title = siteTitle+" | "+$group.titles[$group.current];
			window.location.hash = "&"+$group.titles[$group.current].toLowerCase().stripSpaces();
			setTimeout("scrolling = false",100);
			$events.tileGroupChangeEnd();	
		});	
	
		$mainNav.setActive();
		$events.tileGroupChangeBegin();	
	}
});

/* Set width so we can scroll to last tilegroup */
fixScrolling = function(){
	$("#tileContainer").height(mostDown+100);
}

recalcScrolling = function(){
	mostDown = 0;
	$("#tileContainer").children(".tile").each(function(){
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
	if($("#nav>a").css("display") == "none"){
		$("#nav>a").css("display","block");
	}else{
		$("#nav>a").css("display","none");
	}
});

/* Creates a nice link according to the required page */
makeLink = function(lp){/* To make valid links */
	lp = lp.toLowerCase();
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

function setCookie(c_name,value,exdays){
	var exdate=new Date();
	exdate.setDate(exdate.getDate() + exdays);
	var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
	document.cookie=c_name + "=" + c_value;
}
goToFull = function(){
	if(confirm("You will go to the full site")){
		setCookie("fullsite",1,999);
		window.location.href="index.php";
	}
	return false;
};