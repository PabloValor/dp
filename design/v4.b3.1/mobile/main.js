/* METRO UI TEMPLATE mobile
/* Copyright 2012 Thomas Verelst, http://metro-webdesign.info*/

/*This file does the basic things for the template like loading pages and uses functinos of functions.js*/

$show = {
	prepareTiles: function(){ /* Prepare for showing the tilepage */
		$events.onTilesPrepare();
		$("#subNav").fadeOut(hideSpeed);
		$("#centerWrapper").fadeOut(hideSpeed,function(){
			$show.tiles();
		}); 
		
	},
	tiles: function(){ /* Show homepage */
		$tileContainer = $("#tileContainer")	
		$allTiles = $tileContainer.children(".tile");
		$tileContainer.show().children().hide();
		$("#centerWrapper").show();
		$("#contentWrapper").hide();
		document.title = siteTitle+" - "+siteTitleHome;
		
		if($hashed.parts.length==1 || ($group.current = inArrayNCindex($hashed.parts[1].addSpaces(),$group.titles)) == -1){$group.current = 0;}

		$page.current = "home";
		$tileContainer.addClass("loading")
		$events.beforeTilesShow();
		
		if($group.showEffect==0){	
			$allTiles.each(function(index) {
				var $this = $(this)
				if($this.hasClass("group0")){
					$this.delay(50*index).show(300);
				}else{
					$this.delay(50*index).fadeIn(300);
				}		
			});
		}else if($group.showEffect==1){
			$allTiles.fadeIn(700);
		}else if($group.showEffect==2){
			$allTiles.show(700);
		}
		$tileContainer.children(".groupTitle").fadeIn(700);
		
		setTimeout(function(){
			
			$tileContainer.removeClass("loading")
		 	$(window).resize(); // check the scrollbars now, same as ^
			$events.afterTilesShow();
		},701);
		
		$mainNav.setActive();
		if($group.current > 1){
			$("html, body").animate({scrollTop:$("#groupTitle"+$group.current).offset().top},1000);
		}
		$(window).resize();
	},
	page:function(){ /* show a page with content */
		$("#adminEditButton").attr("href","admin/page-editor.php?p="+$hashed.parts[0]);
		$content = $("#content")
		$("#tileContainer").hide();
		$("#centerWrapper").show();
		$("#contentWrapper").fadeIn(700);
		$content.html("<img src='themes/"+theme+"/img/primary/loader.gif' height='24' width='24'/>");
		$group.current = -1;
		$page.current = "loading";
		
		var title;
		if($hashed.parts[0].substr(0,4) == "url="){ // if the template already noticed the link was not in pageTitles array when generating the url
			title = $hashed.parts[0].substr(4).split(".")[0].addSpaces();
			url = $hashed.parts[0].substr(4);
		}else{ // url is OK
			var hashReq = $hashed.parts[0].addSpaces();
			var i = inArrayNCkey(hashReq,pageURL); // find the corresponding array entry with title
			if(i!=-1){ // found!
				title = pageTitles[i];
				url = i;
			}else{ // not found! let's do a wild guess of the url!
				title = hashReq.split(".")[0];
				url = hashReq+".php";
			}
		}
		submenu = [];
		
		$.ajax("pages/"+url+(typeof $hashed.get[1] != "undefined" ? "?"+$hashed.get[1] : "")).success(function(newContent,textStatus){	
			$content.fadeOut(50,function(){	
				$content.html(newContent);
				$page.current = url;
				transformLinks();
				$subNav.make();
				$events.beforeSubPageShow();
				$content.show(500,function(){
					$events.afterSubPageShow();
					$(window).resize();
				});
				if (typeof _gaq !== "undefined" && _gaq !== null) {_gaq.push(['_trackPageview', "/#!/"+$hashed.parts[0]]); }
			});
		}).error(function(){
			title = l_pageNotFound;
			$content.html(l_pageNotFoundDesc).show(400);
			document.title = title+" | "+siteTitle;
			$subNav.setActive();
		})
		
		document.title = title+" | "+siteTitle;
		$(window).resize();
	}
}

$(window).hashchange(function(){
	$hashed.get = chars(decodeURI(window.location.hash).replace("#!/","").replace("!/","").replace("#!","").replace("#","")).split("?");
	$hashed.parts = $hashed.get[0].split("&"); 
	$events.hashChangeBegin();
	if($hashed.doRefresh){
		if($hashed.parts[0] == ""){ // homepage with tiles
			if($group.current == -1){ // no tiles shown
				if($page.current == ""){
					$show.tiles();
				}else{
					$show.prepareTiles();
				}
			}else{ // it must have been a tilegroup switch
				if($hashed.parts.length>1){
				}else if($group.current == 0){//we refresh the page
					$show.prepareTiles();
				}else{
					$group.goTo(0);
				}		
			}
		}else{ // page with content
			if($page.current == "home"){ // homepage with tiles
				$("#centerWrapper").fadeOut(hideSpeed,function(){
					$show.page();
				});
			}else if($page.current != ""){ // other content page
				$("#content").hide(hideSpeed,function(){
					$show.page();
				});
			}else{ // nothing loaded yet
				$show.page();
			}
		}
	}
	$events.hashChangeEnd();
});


$(window).resize(function(){
	$events.windowResizeBegin();
});

window.onload=function(){
	$tileContainer  = $("#tileContainer");
	
	$events.siteLoad();
		
	/* for fixing dimension issues */
	for(i=0;i<$group.count;i++){
		$tileContainer.children(".group"+i).each(function(){
			var thisDown= parseInt($(this).css("margin-top"))+$(this).height();
			if(thisDown>mostDown){
				mostDown=thisDown;
			}
			/* For nice urls with nice transitions */
			if(typeof $(this).attr("href") != "undefined"){
				$(this).attr("href",$(this).attr("href").replace("?p=","#!/"));
			}		
		})				
	}	
	tileContainer = $("#tileContainer").html();
	
	/*For good scrolling */
	fixScrolling();
	
	/* make links for mainnav for navigation */
	$mainNav.init();
	
	/*Start page rendering */
	setTimeout(function(){
		$(window).hashchange();
	},20);

	/*For main nav*/
	$("#navTitle").click(function(){
		if($("#navItems").css("display") == "none"){
			$("#navItems").css("display","block");
			setTimeout(function(){
				$(document).bind("click.closeNav",function(){
					$("#navItems").css("display","none");
					$(document).unbind("click.closeNav");	
				})
			},1);
		}else{
			$("#navItems").css("display","none");
		}
	});
	
	/*Go to full site */
	$("#tileContainer, footer").on("click",".goToFull",function(){
		if(confirm(l_goToFullSiteRedirect)){
			setCookie("fullsite",1,999);
			window.location.href="index.php";
		}
		return false;
	});
	
	$(window).resize();
};

