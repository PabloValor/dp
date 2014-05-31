<?php
session_start();
require_once("config.php"); 
if($_SESSION['username']!=$username){
	die("It seems you're not logged in anymore. File NOT deleted! Try to reload this page.");
}
if(isset($_POST['file']) ){
	$file = stripslashes($_POST['file']);  
	if(!file_exists("../pages/".$file)){
		die("Error: File doesn't exist!");
	}
	$handle = fopen("../pages/".$file,'r+');
	$content = fread($handle,filesize("../pages/".$file));
	fclose($handle);
	unlink("../pages/".$file);
	$nameArray = explode("/","../pages/".$file);
	$name =end($nameArray);
	while(file_exists('trash/'.$name)){
		$name.="_2";
	}
	$url = 'trash/'.$name;
	$handle = fopen($url,'w+');
	fwrite($handle,$content);
	fclose($handle);
	echo "yes";
}
?>