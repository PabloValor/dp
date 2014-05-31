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
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>Admin Area - Edit file</title>
    <link href='http://fonts.googleapis.com/css?family=Open+Sans:400,300,600' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" type="text/css" href="css/main.css" />
    <link rel="stylesheet" type="text/css" href="css/code-editor.css" />
    
    <script type="text/javascript" language="javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js"></script>
    <script type="text/javascript">window.jQuery || document.write('<script type="text/javascript" src="../js/inc/jquery181.js"><\/script>')</script>
    <script>file = '<?php echo $_GET['p']?>';</script>
	<script type="text/javascript" language="javascript" src="js/code-editor.js"></script>
</head> 
<body class="code-editor">
<div id="admin-headerWrapper">
<h2 id="admin-title">Edit <em><?php echo $url?></em></h2>
<div id="admin-headerLinks">
<a href="home.php">Admin</a> 
 
<a target='_blank' href='../'>Visit site</a>
<a href="../mobile.php" target='_blank'>Visit mobile site</a>
<a id="admin-logoutLink" href="#" onclick='logout();'>Logout</a>
</div>
<div id="admin-options">
<div id="msgbox"></div>
<button id="saveButton">Save</button>
<button id="deleteButton">Delete</button>
</div>
</div>
<?php
if($error == ''){//no errors	 ?>
	<div id="admin-editor"><?php echo $content;?></div>
<?Php
}else{
	echo $error;
}?>
<script src="ace/ace.js" type="text/javascript" charset="utf-8"></script>
<script>
$(document).ready(function(){
	editor = ace.edit("admin-editor");
    editor.setTheme("ace/theme/textmate");
    editor.getSession().setMode("ace/mode/<?php echo $filetype;?>");
	$(window).resize();	
});
</script>
</body>
</html>
