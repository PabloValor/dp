<?php
session_start();
if(!isset($_SESSION['username'])){
	header("Location: index.php");
	die("You are not logged in. Please go to <a href='index.php'>login</a>");
}

if(!isset($_GET['confirm']) ||$_GET['confirm'] != "165"){
	?>
    This will delete your current sitemap!
    <p>If you're sure you want to continue, click <a href="sitemap.php?confirm=165">here</a>
    <?php
}else{
include_once("../config/pages.php");

/*INIT FUNCTIONS */
function chars($r){
	$charSearch = array("/à|á|â|ã|ä|å|æ|À|Á|Â|Ã|Ä|Å|Æ/","/ç|Ç/","/è|é|ê|ë|È|É|Ê|Ë/","/ì|í|î|ï|Ì|Í|Î|Ï/","/ò|ó|ô|õ|ö|ð|ø|Ò|Ó|Ô|Õ|Ö|Ð|Ø/","/œ|Œ/","/ù|ú|û|ü|Ù|Ú|Û|Ü/","/ý|ÿ|Ý|Ÿ/","/š|Š/","/ž|Ž/","/Þ/","/ß/","/ƒ|Ƒ/");
	$charReplace = array("a","c","e","i","o","oe","u","y","s","z","b","ss","f");
	return preg_replace($charSearch, $charReplace, $r);
};
function stripSpaces($s){
	return str_replace(" ","-",$s);
}
function makeLinkHref($l){
	global $pageTitles;
	if($l==""){
		return "";
	}
	if(substr($l,0,9) == 'external:'){
		return substr($l,9);
	}
	
	if(substr($l,0,7) == "http://" ||
	   substr($l,0,8) == "https://" ||
	   substr($l,0,1) == "/" ||
	   substr($l,0,1) == "#" ||
	   $l[strlen($l)-1] == "/")
	{
		return $l;
	}
	if(array_key_exists($l,$pageTitles)){
		$lu = strtolower(chars($pageTitles[$l]));
	}else{
		$lu = strtolower(chars("url=".$l));
	}
	
	return "#!/".stripSpaces($lu);	
}

/* BUILD SITEMAP */
$sitemap = '<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';

/*Homepage */
$sitemap .= '
	<url>
	<loc>'.dirname(dirname("http://" . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'])).'</loc>
	<lastmod>'.date ("Y-m-d", filemtime("../index.php")).'</lastmod>
	<priority>1</priority>
	</url>';

/*Subpages */
foreach($pageTitles as $url=>$pageTitle){
	$sitemap .= '
	<url>
	<loc>'.dirname(dirname("http://" . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'])).'/'.makeLinkHref($url).'</loc>
	<lastmod>'.date ("Y-m-d", filemtime("../pages/".$url)).'</lastmod>
	<priority>0.7</priority>
	</url>';
}

$sitemap .= "
</urlset>"; 

file_put_contents("../sitemap.xml",$sitemap);

?>
Sitemap creation finished. Click <a href="../sitemap.xml">here</a> to open it.
<?php
} // end confirm check if
?>