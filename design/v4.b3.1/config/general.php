<?php
/* GENERAL CONFIG */

$siteTitle = 'Your website'; /* will be displayed above the url-bar / in tab / on Google */
$siteName = 'Your website'; /* The biggest title on your homepage */
$siteDesc ='The description of your website'; /* subtitle on your homepage */
$siteTitleHome = 'Home'; // will be displayed above the url-ba / in tab / in google when the home-page is open
$siteFooter = '© Your name';

$siteMetaDesc = 'A description of your site for Google here';
$siteMetaKeywords = 'Some, keywords, seperated, by, commas, here, max 10';

$favicon_url = "/favicon.ico";

$googleAnalyticsCode = ""; // Your Google Analytics Web Property ID in the form UA-XXXXX-Y or UA-XXXXX-YY. (check: http://support.google.com/analytics/bin/answer.py?hl=en&answer=1032385)

$lang = "en"; // lang of the site (used for locale file! So if you put "nl" you need a file nl.php in the locale folder. (to create such a file: start by copying the default en.php file)

/* Compressing settings */
$compressJS = false; // compress JS
$compressCSS = false; // compress CSS
$autoFlush = true;
$autoFlushPlugins = true;

$compressJS_mob = false; // compress JS of mobile site
$compressCSS_mob = false; // compress CSS of mobile site
$autoFlush_mob = true;
$autoFlushPlugins_mob = true;

/* Plugin settings*/
$disabledPluginsDesktop = array(); // add the folder names here if you want to specifically disable plugins on the main (full/desktop) site
$disabledPluginsMobile = array(); // add the folder names here if you want to specifically disable plugins on the mobile site

?>