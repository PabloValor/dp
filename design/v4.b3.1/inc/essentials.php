<div id="subNavTemp">
<div id="subNav">
<?php
set_include_path("../");
include_once("defaults.php");
include_once("config/pages.php");
include_once("init.php");
if(isset($subNav)){
	foreach($subNav as $navItem){
		$navItem = explode(";",$navItem);
		echo "<a style='background-color: ".$navItem[2].";' ".makeLink(trim($navItem[1])).">".trim($navItem[0])."</a>";
	}
}
?>
</div>
</div>

<?php
function metroLink($url){
	echo " ".makeLink(trim($url))." rel='metro-link' ";
}
?>