<?php
/* Default settings, not recommend to change this, use the config folder instead! */

/*GENERAL*/
$siteTitle = 'Your website'; /* will be displayed above the url-bar / in tab / on Google */
$siteName = 'Your website'; /* The biggest title on your homepage */
$siteDesc ='A description of your site'; /* subtitle on your homepage */
$siteTitleHome = 'Home'; // will be displayed above the url-ba / in tab / in google when the home-page is open
$siteFooter = '(c)your name';

$siteMetaDesc = 'A description of your site for Google here';
$siteMetaKeywords = 'Some, keywords, seperated, by, commas, here, max 10';

$favicon_url = "/favicon.ico";

$googleAnalyticsCode = ""; // Your Google Analytics Web Property ID  (check: http://support.google.com/analytics/bin/answer.py?hl=en&answer=1032385)

$lang = "en";

/* Tile options */
$scale = 145; // size of 1 tile of 1x1, in px
$spacing = 10; // space between tiles, in px

$groupTitles = array('Group 1','Group 2','Group 3'); // titles of the tileGroups
$groupSpacing = array(4,4,4); // width of each tileGroup (spacing between the groups in tiles)

$showSpeed = 400; // speed of the showing transition
$hideSpeed = 300; // hide speed of page transitions


/* Page array */
$pageURL = array(); // required, necessary
$pageTitles = array(); // required, necessary
$pageDescriptions = array(); // not required, not really necessary
$pageKeywords = array(); // not required, not really necessary

/*Compressing settings */
$compressJS = false;
$compressCSS = false;
$autoFlush = true;
$autoFlushPlugins = true;
$onlyCombineJS = false;
$onlyCombineCSS = false;
$compressJS_mob = false;
$compressCSS_mob = false;
$autoFlush_mob = true;
$autoFlushPlugins_mob = true;
$onlyCombineJS_mob = false;
$onlyCombineCSS_mob = false;

/*Plugin settings*/
$disabledPluginsDesktop = array();
$disabledPluginsMobile = array();

/* LAYOUT */
$theme = "theme_default"; // name of the subfolder in themes directory for the theme you want

$font = ""; // leave blank if you want to use the default one, otherwise  ex:  "'Open Sans', Segoe UI light, Tahoma,Helvetica,sans-serif"
$googleFontURL = "http://fonts.googleapis.com/css?family=Open+Sans:400,300,600"; // leave blank if you don't want a special one

/* Tilegroup settings */
$scrollSpeed = 550; // scrolling speed of tilegroups
$groupInactiveOpacity = 1; // opacity of tiles that are not in the current tilegroup. 1 = full shown, 0.5 = transparent, can have any value between 0 and 1
$groupInactiveClickable = true; // should the tiles in inactive groups be clickable, if false; it'll go to the tilegroup of the clicked tile
$groupShowEffect=0; // the effect which shows the tiles when the page is loaded. 0 = a nice "wave" effect, 1 = fadeIn, 2= increase size
$groupDirection = "horizontal"; // put the groups in a vertical or horizontal order?
$mouseScroll = true; // disable or enable scrolling with mousewheel

/* Background */
$bgColor = "#DDD"; // background color of the page
$bgImage = ""; // background image, leave blank if you dont want one

$bgMaxScroll = 150; //set to 0 for no scrolling
$bgWidth = 115; // in procent, in comparison to the screen width, so 125% is a quarter bigger than screen ,needed for scrolling, how bigger, how more scrolling
$bgScrollSpeed = 450; // in ms

/* Some behavior */
$scrollHeader = true; // wether the header should scroll with the page (true) or always stay visible (false)
$scrollHeaderTablet = false; // otherwise laggy
$disableGroupScrollingWhenVerticalScroll = false; // if the page is too high and not all tiles fit on screen, mousewheel triggers vertical scroll instead of tilegroup scroll. Set to false if you want always to have groupScrolling

$autoRearrangeTiles = true; // auto rearrange tiles when it doesn't fit on the browser?
$autoResizeTiles = true; // auto resize tiles when it doesn't fit on the browser? Can cause markup problems!, will only work if $autoRearrangeTiles is enabled
$autoRearrangeEffect = true; // if true, nice transition effect is used when rearranging tiles. Can be laggy if page is heavy, so disable it then.
$rearrangeTreshhold = 3;  // from which width the tiles should be rearranged? Just play with this value! Should be smaller than the most wide tilegroup.

$maxPageWidth=900;


/* MOBILE */
$enableMobile = true; // enable mobile version of template
$redirectPhone = true; // redirect phones
$redirectTablet = false; //redirect tablets

$groupSpacing_mob = array(4,4,4);

$mobileZoomable = false; // enable pinch-to-zoom or not?
$showFullSiteLink = true; // show link to full site in footer of mobile site

$indexMobileSite = false;


/*CHARACTERS*/

?>