<?php
/* LAYOUT CONFIG */

$theme = "theme_default"; // name of the subfolder in themes directory for the theme you want

$font = ""; // leave blank if you want to use the default one, otherwise  ex:  "'Open Sans', Segoe UI light, Tahoma,Helvetica,sans-serif"
$googleFontURL = "http://fonts.googleapis.com/css?family=Open+Sans:400,300,600"; // leave blank if you don't want a special one

$maxPageWidth=900; // max width of page in px

/* Tile options */
$scale = 145; // size of 1 tile of 1x1, in px
$spacing = 10; // space between tiles, in px

/* Tilegroup settings */
$groupTitles = array('Home','Second tilegroup','Group 3'); // titles of the tileGroups
$groupSpacing = array(4,4,3); // width of each tileGroup (spacing between the groups in tiles)
$groupDirection = "horizontal"; // put the groups in a vertical or horizontal order?
$mouseScroll = "groups"; //  set to "groups" to scroll between groups, set to "horizontal" to continuously scroll horizontal or set to false to disable scrolling (so it will scroll vertical)

$scrollSpeed = 550; // scrolling speed of tilegroups
$groupInactiveOpacity = 1; // opacity of tiles that are not in the current tilegroup. 1 = full shown, 0.5 = transparent, can have any value between 0 and 1
$groupInactiveClickable = true; // should the tiles in inactive groups be clickable, if false; it'll go to the tilegroup of the clicked tile
$groupShowEffect=0; // the effect which shows the tiles when the page is loaded. 0 = a nice "wave" effect, 1 = fadeIn, 2= increase size  (!only works when $groupInactiveOpacity = 1)

$showSpeed = 400; // speed of the showing transition
$hideSpeed = 300; // hide speed of page transitions

/* Background */
$bgColor = "#0F6D32"; // background color
$bgImage = "img/bg/metro_green.jpg"; // background image, leave blank if you dont want one. It is recommend to keep the filesize to a minimum and also, if possible, use a low resolution

// Settings below are only needed when $bgScrollType is parallax
$bgMaxScroll = 130; //set to 0 for no background scrolling
$bgWidth = 115; // in procent, in comparison to the screen width, so 125% is a quarter bigger than screen ,needed for scrolling, how bigger, how more scrolling
$bgScrollSpeed = 450; // in ms (recommend to set this to $scrollSpeed-10) 

/* Some behavior */
$scrollHeader = true; // wether the header should scroll with the page (true) or always stay visible (false)
$scrollHeaderTablet = false; // otherwise laggy
$disableGroupScrollingWhenVerticalScroll = false; // if the page is too high and not all tiles fit on screen, mousewheel triggers vertical scroll instead of tilegroup scroll. Set to false if you want always to have groupScrolling

$autoRearrangeTiles = true; // auto rearrange tiles when it doesn't fit on the browser?
$autoResizeTiles = true; // auto resize tiles when it doesn't fit on the browser? Can cause markup problems!, will only work if $autoRearrangeTiles is enabled
$autoRearrangeEffect = true; // if true, nice transition effect is used when rearranging tiles. Can be laggy if page is heavy, so disable it then.
$rearrangeTreshhold = 2;  // from which width the tiles should be rearranged? Just play with this value! Should be smaller than the most wide tilegroup.

/*Defaults for tiles*/
$defaultBackgroundColor = "#509601";
$defaultLabelColor = "#476327";
$defaultLabelPosition = "top";


?>