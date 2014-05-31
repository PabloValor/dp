<?php
session_start();
if(!isset($_SESSION['username'])){
	header("Location: index.php");
	die("You are not logged in. Please go to <a href='index.php'>login</a>");
}

/* INIT ALL CONFIGS ETC*/

require_once('../inc/defaults.php');
require_once('../config/general.php');
require_once('../config/layout.php');
require_once('../config/pages.php');
require_once('../inc/init.php');

$error = '';
$content = '';
$filetype = '';

if(!isset($_GET['p'])){
	die("Editing error: no page requested");
}
/*Messy code */
if(isset($_GET['p'])){
	$url = $_GET['p']; 
	if(substr($url,0,4) == "url="){ // not in pageTitles array
		$url = substr($url,4);
	}else{
		$pos = array_search(strtolower($url), array_map('strtolower',$pageTitles));
		if($pos != false){
			$url = $pos;
		}
	}
	$parts = pathinfo($url);
	$ext = $parts['extension'];
	switch($ext){
			case "htm":
			case "html":
			$filetype = 'html';
			break;
			case "php":
			$filetype = 'php';
			break;
			case "js":
			$filetype = 'javascript';
			break;
			case "css":
			$filetype = 'css';
			break;
			case "xml":
			$filetype = 'xml';
			break;
			default:
			$filetype = 'html';
			break;
	}
	if(file_exists("../pages/".$url) && trim($url) != ""){
		if(filesize("../pages/".$url) ==0){
			$content = "";
		}else{
			$handle = fopen("../pages/".$url, "r+") or die("Can't open file");
			$content = htmlentities(fread($handle,filesize("../pages/".$url)));
		}
	}else{
		$error = "File not found. Please go to <a href='index.php'>Index</a>";
	}
}else{
	$error =  "No file specified. Please go to <a href='index.php'>Index</a>";
}
$siteLink = makeLinkHref($url);
$siteLinkAjax = str_replace("?p=","#!/",$siteLink);

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>Admin Area - Edit file</title>
	 <?php if($googleFontURL != ""){?>
    	<link href='<?php echo $googleFontURL?>' rel='stylesheet' type='text/css'>
		<?php
	}
	?>
    
    <link rel="stylesheet" type="text/css" href="../css/layout.css" />
    <link rel="stylesheet" type="text/css" href="css/main.css" />
    <link rel="stylesheet" type="text/css" href="css/page-editor.css" />
    <link rel="stylesheet" type="text/css" href="../themes/<?php echo $theme?>/theme.css" />
    <script type="text/javascript" language="javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js"></script>
    <script type="text/javascript">window.jQuery || document.write('<script type="text/javascript" src="../js/inc/jquery181.js"><\/script>')</script>
    <script>file = '<?php echo $url?>';</script>
	<script type="text/javascript" language="javascript" src="js/page-editor.js"></script>
</head> 
<body class="page-editor" style="background-color:<?php echo $bgColor;?>;">
<div id="admin-headerWrapper">
<h2 id="admin-title">Edit <em><?php echo $url?></em></h2>
<div id="admin-headerLinks">
<a href="home.php">Admin</a> 
 
<a target='_blank' href='../<?php echo $siteLinkAjax?>'>Visit site</a>
<a target='_blank' href='../mobile.php<?php echo $siteLinkAjax?>'>Visit mobile site</a>
<a id="admin-logoutLink" href="#" onclick='logout();'>Logout</a>
</div>
<table id="admin-options">
<tr><td>
Left side width 
</td>
<td><input type="text" id="leftWidth" style="width:15px;" value="40" />%</td>
<td><button id="saveButton">Save</button></td>
<td><div id="msgbox"></div></td>
</tr>
<tr>
<td>Live editing </td>
<td><input type="checkbox" id="enableLive" checked="checked" /></td>

<td><button id="previewNow">Preview</button></td>
<td><button id="deleteButton">Delete</button></td>
</tr>
</table>
</div>
<?php
if($error == ''){//no errors	 ?>
	<div id="admin-editor"><?php echo $content;?></div>
    <div id="contentWrapper">
    	<div id="content"></div>
      </div>
<?Php
}else{
	echo $error;
}?>
<script src="ace/ace.js" type="text/javascript" charset="utf-8"></script>
</body>
</html>
