<?php
session_start();
require_once("../config.php"); 
if($_SESSION['login']!=$adminLogin){
	die("It seems you're not logged in anymore. Flushing failed.");
}

$handle = fopen("../cache/compressed.css","w") or die("Can't flush cache of css files");
fclose($handle);
unlink("../cache/compressed.css")  or die("Can't flush cache of css files");

$handle = fopen("../cache/compressed.js","w") or die("Can't flush cache of javascript files");
fclose($handle);
unlink("../cache/compressed.js")  or die("Can't flush cache of javascript files");

$handle = fopen("../cache/latestedit.txt","w") or die("Can't flush latestedit.txt file");
fclose($handle);
unlink("../cache/latestedit.txt")  or die("Can't flush latestedit.txt file");

if(file_exists("../cache/compressed-mob.css")){
	$handle = fopen("../cache/compressed-mob.css","w") or die("Can't flush cache of css files  for mobile version");
	fclose($handle);
	unlink("../cache/compressed-mob.css")  or die("Can't flush cache of css files for mobile version");
}
if(file_exists("../cache/compressed-mob.js")){
	$handle = fopen("../cache/compressed-mob.js","w") or die("Can't flush cache of javascript files for mobile version");
	fclose($handle);
	unlink("../cache/compressed-mob.js")  or die("Can't flush cache of javascript files for mobile version");
}
if(file_exists("../cache/no-js-mob.txt")){/*FLUSH NO-JS CACHE / ONLY FOR MOBILE VERSION */
	$handle = fopen("../cache/no-js-mob.txt","w") or die("Can't flush cache of javascript files for mobile version");
	fclose($handle);
	unlink("../cache/no-js-mob.txt")  or die("Can't flush cache of javascript files for mobile version");
}
if(file_exists("../cache/latestedit-mob.txt")){
	$handle = fopen("../cache/latestedit-mob.txt","w") or die("Can't flush latestedit-mob.txt file");
	fclose($handle);
	unlink("../cache/latestedit-mob.txt")  or die("Can't flush latestedit-mob.txt file");
}
echo "yes";
?>