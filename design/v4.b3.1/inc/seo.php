<?php
/*SEO OPTIMIZATION */
$reqUrl = "";
$nojsuser = false;
if(isset($_GET['_escaped_fragment_']) || isset($_GET['p'])){ /* If Google is crawling our pages */
    $bot = true; /* The bot is here! */
    if(isset($_GET['_escaped_fragment_'])){
		$pages = explode("&",$_GET['_escaped_fragment_']);
	}else if(isset($_GET['p'])){
		$pages = explode("&",$_GET['p']);
		$nojsuser = true;
	}
	$page = str_replace("-"," ",$pages[0]);
	$page= str_replace("..","",$page);
	$page= str_replace("/","",$page); /* Get the page he wants from the url */
	
	/*Fake our menu for crawling*/
	$links = "<a class='subNavItem' style='background-color:#C33;' href='#!'>".$l_home."</a>";
	foreach($pageTitles as $i => $name){
		$links .= "<a class='subNavItem' style='background-color:#C33;' href=#!/".str_replace(" ","-",$name).">".$name."</a>";
	}
	
	if($page == "" || $page == "home"){	
		$reqUrl = "";
		$siteTitle = $siteTitle." | ".$siteTitleHome;		
	}else{
		if(substr($page,0,4) == "url=" && file_exists("pages/".strtolower(substr($page,4)))){
			$reqUrl = strtolower(substr($page,4));
			$siteTitle = $reqUrl." | ".$siteTitle;
		}else{
			foreach($pageURL as $url=>$pageURLs){
				if(strtolower(chars($pageURLs)) == strtolower(chars($page))){
					$reqUrl = $url;
					$siteTitle = $pageTitles[$url]." | ".$siteTitle;
					break;
				}
			}
			if($reqUrl == ""){
				if(file_exists("pages/".strtolower($page).".php")){
					$reqUrl = strtolower($page).".php";
					$siteTitle = $page." | ".$siteTitle;
				}else{
					$reqUrl = "pagenotfound";
				}
			}
			if(isset($pageDescriptions[$reqUrl])){
				$siteMetaDesc = $pageDescriptions[$reqUrl];
			}
			if(isset($pageKeywords[$reqUrl])){
				$siteMetaDesc = $pageKeywords[$reqUrl];
			}
		}
	}	
}else{$bot = false;}
?>