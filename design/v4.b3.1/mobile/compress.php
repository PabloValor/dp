<?php

/* AUTO FLUSH CACHE SYSTEM */
if($autoFlush == true){
	if($autoFlushPlugins){
		$cssFiles = array_merge($cssFiles,$cssPluginsArray);
		$jsFiles = array_merge($jsPluginsArray,$jsFiles);
	}	
	$fileAge = 0;
	if($compressCSS_mob){
		foreach($cssFiles as $cssFile){
			$fileAge += filemtime($cssFile);
		}		
	}
	if($compressJS_mob){
		foreach($jsFiles as $jsFile){
			$fileAge += filemtime($jsFile);
		}
	}
	if(file_exists("cache/latestedit-mob.txt")){
		$oldFileAge = file_get_contents("cache/latestedit-mob.txt");
		if($oldFileAge=="" || $fileAge>$oldFileAge){
			$handle = fopen("cache/latestedit-mob.txt", "w");
			fwrite($handle,$fileAge);
			flushCache();
		}
	}else{
		$handle = fopen("cache/latestedit-mob.txt", "w");
		fwrite($handle,$fileAge);
		flushCache();
	}
	if($autoFlushPlugins){
		if(file_exists("cache/compressfilescount-mob.txt")){
			$filesCount = file_get_contents("cache/compressfilescount-mob.txt");
			if($filesCount == "" || (int)$filesCount != count($cssFiles)*$compressCSS_mob+count($jsFiles)*$compressJS_mob){
				flushCache();
			}
		}else{
			flushCache();
		}
	}
}

if(!$autoFlushPlugins){
	$cssFiles = array_merge($cssFiles,$cssPluginsArray);
	$jsFiles = array_merge($jsPluginsArray,$jsFiles);
}

$totalFiles = 0;
/*CSS COMPRESS*/
$css = '';
if($compressCSS_mob){
	if(!file_exists("cache/compressed-mob.css")){
		$totalFilesHandle = fopen("cache/compressfilescount-mob.txt",'w');
		$handle = fopen("cache/compressed-mob.css",'w');	
		$compressedCss = '';
		foreach ($cssFiles as $cssFile) {
	  		$compressedCss .= file_get_contents($cssFile);
		}
		if(!$onlyCombineCSS_mob){
			$compressedCss = preg_replace('!/\*[^*]*\*+([^/][^*]*\*+)*/!', '', $compressedCss);// Remove comments
			$compressedCss = str_replace(': ', ':', $compressedCss);// Remove space after colons
			$compressedCss = str_replace(array("\r\n", "\r", "\n", "\t", '  ', '    ', '    '), ' ', $compressedCss);// Remove whitespace
		}
		fwrite($handle,$compressedCss);
		$totalFiles+=count($cssFiles);
		fwrite($totalFilesHandle,$totalFiles);
	}
	$css = '<link rel="stylesheet" type="text/css" href="cache/compressed-mob.css" />';
}else{
	foreach($cssFiles as $cssFile){
		$css .= '<link rel="stylesheet" type="text/css" href="'.$cssFile.'" />';
	}
}
/*JAVASCRIPT COMPRESS*/
$js = '';
if($compressJS_mob){
	if(!file_exists("cache/compressed-mob.js")){
		require_once('inc/jsminplus.php');
		$totalFilesHandle = fopen("cache/compressfilescount-mob.txt",'w');
		$handle = fopen("cache/compressed-mob.js",'w');	
		$compressedJs = '';
		foreach ($jsFiles as $jsFile) {
	  		$compressedJs .= file_get_contents($jsFile)."\n";
		}
		if(!$onlyCombineJS_mob){
			$compressedJs = JSMinPlus::minify($compressedJs);
		}
		fwrite($handle,$compressedJs);	
		$totalFiles+=count($jsFiles);
		fwrite($totalFilesHandle,$totalFiles);
	}
	$js = '<script type="text/javascript" src="cache/compressed-mob.js" /></script>';
}else{
	foreach($jsFiles as $jsFile){
		$js .= '<script type="text/javascript" src="'.$jsFile.'" /></script>';
	}
}

/*FUNCTION FLUSHCACHE*/
function flushCache(){
	if(file_exists("cache/compressed-mob.css")){
		$handle = fopen("cache/compressed-mob.css","w") or die("Can't flush cache of css files");
		fclose($handle);
		unlink("cache/compressed-mob.css")  or die("Can't flush cache of css files");
	}
	if(file_exists("cache/compressed-mob.js")){
		$handle = fopen("cache/compressed-mob.js","w") or die("Can't flush cache of javascript files");
		fclose($handle);
		unlink("cache/compressed-mob.js")  or die("Can't flush cache of javascript files");
	}
}
?>