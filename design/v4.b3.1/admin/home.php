<?php
session_start();
if(!isset($_SESSION['username'])){
	header("Location: index.php");
	die("You are not logged in. Please go to <a href='index.php'>login</a>");
}
$valid_ext = array("TXT","txt","htm","HTM","html","HTML","shtm","SHTM","shtml","SHTML","pl","PL","cgi","CGI","CSS","css","conf","CONF","ASP","asp","JSP","jsp","js","JS","php","PHP","php3","PHP3","PHTML","phtml","ini","INI","cfm","CFM","inc","INC","xml","XML");

function drawFolder($dir,$valid_ext){
	drawLinks(glob($dir."*.*"),$valid_ext);
	$folders = glob($dir . "*");
	foreach($folders as $folder){
		drawLinks(glob($folder."/" . "*.*"),$valid_ext);
	}
}
function drawLinks($pages,$valid_ext){
	if(!empty($pages)){
		foreach($pages as $page){
			$page = substr($page,2);
	    	$ext = substr(strrchr($page, '.'), 1);
			$pageText = "<span style='font-size:11px;'><em>".substr($page, 0, strrpos( $page, '/') )."/</em></span>&nbsp;".substr(strrchr($page, '/'), 1);
			if (in_array($ext,$valid_ext) && is_writable("../".$page)) {
				echo '<a class="pageLink" title="Edit now!" href="code-editor.php?p='.'..'.$page.'">'.$pageText.'</a><br />';
			}
		}
	}
}


?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>Admin Area - Overview</title>
	<link rel="stylesheet" type="text/css" href="css/main.css" />
	<link rel="stylesheet" type="text/css" href="css/home.css" />
	<script type="text/javascript" language="javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js"></script>
    <script type="text/javascript">window.jQuery || document.write('<script type="text/javascript" src="../js/inc/jquery181.js"><\/script>')</script>
	<script type="text/javascript" language="javascript" src="js/main.js"></script>
    <script type="text/javascript" language="javascript" src="js/home.js"></script>
</head> 
<body>
<div id="headerWrapper"><div id="header">
<h1>
<a href="home.php">Admin</a>  
<a href="../" target='_blank' style='font-size:16px; margin-left:30px;'>Visit site</a>
<a href="../mobile.php" target='_blank' style='font-size:16px; margin-left:30px;'>Visit mobile site</a> 
<a href="sitemap.php" target='_blank' style='font-size:16px; margin-left:30px;'>Build Sitemap</a>
</h1>
<a id="logoutLink" href="#" onclick='logout();'>Logout</a>
</div></div>
<div id="wrapper">
	
<table width="100%" >
    <thead valign="top" align="left">
    <tr >
		<th style='width:50%;'>
			<h2>Your Pages</h2>
    	</th>
        <th>
        	<h2>Other Files</h2>
        </th>
        <th>
        </th>
   </tr>
   </thead>     
   <tbody>
   <tr valign="top">
   <td style='padding:0 10px;'>
		<?php
		//get all pages
				
		$pages = glob("../pages/*.*");
		if(!empty($pages)){
			foreach($pages as $page){
				$page = substr($page,2);
		    	$ext = substr(strrchr($page, '.'), 1);
				$pageText = "<span style='font-size:11px;'><em>pages/</em></span>&nbsp;".substr(strrchr($page, '/'), 1);
				if (in_array($ext,$valid_ext) && is_writable("../".$page)) {
					echo '<a class="pageLink" title="Edit now!" href="page-editor.php?p='.substr($page,7).'">'.$pageText.'</a><br />';
				}
			}
		}
		
		$folders = glob("../pages/*");
		foreach($folders as $folder){
			$pages = glob($folder."/" . "*.*");
			if(!empty($pages)){
				foreach($pages as $page){
					$page = substr($page,2);
		    		$ext = substr(strrchr($page, '.'), 1);
					$pageText = "<span style='font-size:11px;'><em>".substr($page, 0, strrpos( $page, '/') )."/</em></span>&nbsp;".substr(strrchr($page, '/'), 1);
					if (in_array($ext,$valid_ext) && is_writable("../".$page)) {
						echo '<a class="pageLink" title="Edit now!" href="page-editor.php?p='.substr($page,7).'">'.$pageText.'</a><br />';
					}
				}
			}
		}
		
		?><br />
	    <a href="#" id="newPage">New page</a>
	    <div id="newPageWrapper"><em>The page will be made in /pages/ directory</em><br /><br />
	      filename: <input id="newPageName" size="25"/><br /><br />
	    <button id="newPageSubmit">Create</button><span id="newPageMsgbox"></span>
	    </div>
   </td><td style='padding:0 10px;' width="50%">
  		<h3  style='margin-top:0px;'>Config</h3>
        <?php
		drawFolder("../config/",$valid_ext);
		?>
	    <br />
	    <h3>Javascript</h3>
	    <?php
		drawFolder("../js/",$valid_ext);
		?>
	    <br />
	    <h3>CSS</h3>
	    <?php
		drawFolder("../css/",$valid_ext);
		?><br />
        
    </td><td style='padding:0 10px;' width="50%">
    	<h3 style='margin-top:0px;'>Root</h3>
	    <?php
		$directory = "../";
		drawLinks(glob($directory . "*.*"),$valid_ext);
		?><br /> 
        <h3>Mobile</h3>
	    <?php
		drawFolder("../mobile/",$valid_ext);
		?><br /> 
        
        
          
	    <h3>Path</h3>
	    <form id="goPathForm"><input id="goPathLink" size="40" /><button type="submit" id="goPathSubmit">Open</button></form>
    </td></tr></tbody></table>
    
    <hr />
    <table width="100%">
    <tr><td colspan="2" width="50%"><h2>Plugins</h2></td><td colspan="2" width="50%"><h2>Themes</h2></td></tr>
    <tr valign="top">
    <td width="25%">
    <h3 style="margin-top:0;">Config</h3>    
    <?php
	$folders = glob("../plugins/*");
	foreach($folders as $folder){
		if(file_exists($folder."/settings.php")){
			if (is_writable($folder."/settings.php")) {
				echo '<a class="pageLink" title="Edit now!" href="code-editor.php?p='.$folder."/settings.php".'">'.str_replace("../plugins/","",$folder).'</a><br />';
			}
		}
	}
	?>
    </td><td>
   	<h3 style="margin-top:0;">Files</h3>
    <?php
	$folders = glob("../plugins/*");
	foreach($folders as $key=>$folder){
		echo "<a href='#' id='plugindir".$key."' class='plugindirs'>".$folder."</a><div class='pluginfiles' id='pluginlink".$key."'>";
		drawFolder($folder."/" . "*",$valid_ext);
		echo "</div>";
	}
	?>
    </td>
    <td>
    <h3 style="margin-top:0;"">Files</h3>
    <?php
	$folders = glob("../themes/*");
	foreach($folders as $key=>$folder){
		echo "<a href='#' id='themedir".$key."' class='themedirs'>".$folder."</a><div class='themefiles' id='themelink".$key."'>";
		drawFolder($folder."/" . "*",$valid_ext);
		echo "</div>";
	}
	?>
    </td>
    </tr>
    </table>
    <hr />
    <h2>Compressing</h2>
    <em>This framework can compress and combine CSS and JS files. By compressing they have a smaller size and it makes your site faster to load. The framework caches the compressed files and wont make any changes to your original files, so you can edit them. The script should detect when a file is changed to update the cache. If you don't see your change, try pressing the 'Flush Cache' button. If you have the no-javascript version enabled, you must click "Rebuild NoJS" everytime you did a change to the tile config of the mobile version. To enable caching, open config.php in the root folder and set $enableCompressionCss and/or $enableCompressionJs to true.</em>
    <br /><br />
    <button id="flushCacheButton" >Flush cache!</button>
    <span id='flushMsgbox'></span>
</div>
<a id="footer" href="http://metro-webdesign.info" target="_blank">©Thomas Verelst; only for donators</a>
<!-- Please leave this line -->
</body>
</html>
