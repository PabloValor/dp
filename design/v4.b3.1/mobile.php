<?php
session_start();
/* METRO UI TEMPLATE v4 MOBILE
/* Copyright 2012 Thomas Verelst, http://metro-webdesign.info
/* Do not redistribute or sell this template, nor claim this is your own work. 
/* Donation required when using this. */

require_once('inc/defaults.php');
require_once('admin/config.php');

/* Get language */
require_once("inc/locale.php"); // Load default locale
if(file_exists("locale/".$lang.".php")){
	require_once("locale/".$lang.".php");
};

/* Include config files */
require_once('config/general.php');
require_once('config/layout.php');
require_once('config/pages.php');
require_once('config/mobile.php');

/* Get language */
require_once("inc/locale.php"); // Load default locale

/* Device */
$mobile = true;
$tablet = false; // lets asume it's not a tablet (tablets should be on the main version)
$device = "mobile";

setcookie("fullsite",0,7);

/*Tile inits */
require_once('inc/init.php');
require_once('inc/tilefunctions.php');

require_once("inc/plugins.php");

/* FILES*/
$cssFiles = array( /* Add your css files to this array */
	'css/layout.css',
	'css/nav.css',
	'css/tiles.css',
	'themes/'.$theme.'/theme.css',	
	'themes/'.$theme.'/theme-mob.css',	
	'mobile/mobile.css',
);
$jsFiles = array( /* Add your js files to this array */
	'mobile/functions.js',
	'mobile/main.js',
);

/* PLUGIN SYSTEM */
foreach(glob("plugins/" . "*") as $folder){
	if(is_dir($folder) && !in_array($folder, $disabledPluginsMobile)){
		if(file_exists($folder."/plugin.js")){
			$jsPluginsArray[] = $folder."/plugin.js";		
		}
		if(file_exists($folder."/plugin.css")){
			$cssPluginsArray[] = $folder."/plugin.css";		
		}
		if(file_exists($folder."/mobile.js")){
			$jsPluginsArray[] = $folder."/mobile.js";		
		}
		if(file_exists($folder."/mobile.css")){
			$cssPluginsArray[] = $folder."/mobile.css";		
		}
		if(file_exists($folder."/plugin.php")){
			include($folder."/plugin.php");
		}
	}
}

triggerEvent("beforeDoctype");
?>
<!DOCTYPE html>
<?php
triggerEvent("afterDoctype");


if(file_exists('themes/'.$theme.'/theme.js')){
	$jsFiles[] = 'themes/'.$theme.'/theme.js';
}
if(file_exists('themes/'.$theme.'/theme.php')){
	require_once('themes/'.$theme.'/theme.php');
}

triggerEvent("fileInclude");

require_once("mobile/compress.php");
require_once("inc/seo.php");
?>
<html>
<head>
	<?php triggerEvent("headStart");?>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="Description" content="<?php echo $siteMetaDesc;?>"/>
    <meta name="keywords" content="<?php echo $siteMetaKeywords;?>"/>
    <link rel="icon" type="image/ico" href="<?php echo $favicon_url;?>"/>
    <meta name="viewport" content="width=320, target-densitydpi=150, initial-scale=0.999 <?php if(!$mobileZoomable){ echo ", user-scalable=no";}?>">
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <title><?php echo $siteTitle;?></title> 
   
   	<?php 
	if(($bot) || !$indexMobileSite){
		echo '<META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">';
	}
	if($googleFontURL != ""){?>
    	<link href='<?php echo $googleFontURL?>' rel='stylesheet' type='text/css'>
		<?php
	}

	echo $css;
	include_once("inc/css.php");
	
	if($googleAnalyticsCode != ""){
		?><script type='text/javascript'>var _gaq = _gaq || [];_gaq.push(['_setAccount', '<?php echo $googleAnalyticsCode?>']);_gaq.push(['_trackPageview']);(function(){var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);})();</script><?php
	}
	?> 
    <!--[if IE]>
    <script src="js/html5.js"></script>
    <![endif]-->
     <!--[if lt IE 9]>
    <script type="text/javascript" language="javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script src="js/html5.js">
	<![endif]-->
	<!--[if gte IE 9]><!-->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
    <script src="js/html5.js">
	<![endif]-->
    <!--[if !IE]>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
	<![endif]-->

    <script type="text/javascript">window.jQuery || document.write('<script type="text/javascript" src="js/jquery1102.js"><\/script>')</script> 
    <script type="text/javascript" language="javascript" src="js/plugins.js"></script>
	<?php 	
	include("inc/phptojs.php");
    if(!$bot){
		echo $js;
	}
	?>
    <noscript><style>#tileContainer{display:block}</style></noscript>
    <?php
    triggerEvent("headEnd");
	?>
</head>
<body class="mobile">
<?php 
triggerEvent("bodyBegin");

/* BG image */
if($bgImage!=""){	
    echo "<img src='".$bgImage."' id='bgImage'/>";
}
?>
<header>
	<div id="headerWrapper">
		<div id="headerCenter">
			<div id="headerTitles">
				<h1><a href="<?php if($bot){echo "mobile.php";}?>#!"><?php echo $siteName?></a></h1>
		   		<h2><?php echo $siteDesc;?></h2>
		    </div>
		</div>
    </div>
    <?php triggerEvent("headerEnd");?>
</header>
<nav>
	<div id="navTitle"><?php echo $l_menu?></div>
    <div id="navItems">
    <?php
	triggerEvent("mainNavBegin");
	include_once("config/main-nav.php");
	triggerEvent("mainNavEnd");
	?>
    </div>
</nav>
<div id="wrapper">
	<div id="centerWrapper"> 
    		<?php
			//if(!$bot || ($bot && $reqUrl == "")){
			?>
            <div id="tileContainer" <?php if($bot && $reqUrl != ""){ echo "style='display:none;'";}?>>
	       		<?php 
				include("inc/tilegen.php");
				triggerEvent("tileContainerEnd");
				?>
            </div>
            <?php
			//}
			?>
    		<div id="contentWrapper" <?php if($bot && $reqUrl != ""){ echo "style='display:block;'";}?>>  
		   		<?php triggerEvent("contentWrapperBegin");?>
            	<div id="content">	        	
					<?php	
					if($bot){
						if($page == "" || $page == "home"){					
						}else{
							if(file_exists("pages/".$reqUrl)){	
								include("pages/".$reqUrl);
							}else{		
								echo $l_pageNotFoundDesc;
							}
						}
					}
					?>
                	
	        	</div>
                <footer>
					<?php 
					echo $siteFooter; 
					if($showFullSiteLink){
						echo " | <a href='#' class='goToFull'>".$l_goToFullSite."</a>";
					}
					triggerEvent("siteFooter");
					?>
			    </footer>
    	    	<?php triggerEvent("contentWrapperEnd");?>
			</div>
        <?php triggerEvent("centerWrapperEnd");?>
    </div>
    <?php triggerEvent("wrapperEnd");?>
</div>
<?php triggerEvent("bodyEnd");?>
</body>
</html>