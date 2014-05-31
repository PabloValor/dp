<?php
if(!isset($mobile)){
	$mobile = false;
}

/* calculates margin left and top for tiles */
if($mobile){
	require_once("config/tiles-mob.php");
	function getMarginLeft($group){
		return 0;
	}	
	function getMarginTop($group){
		global $scaleSpacing,$groupSpacing_mob;
		$s=0;
		for($i=0;$i<$group;$i++){
			if(count($groupSpacing_mob)>$i){ // if in array (to prevent errors);
				$s+=$groupSpacing_mob[$i];
			}else{
				$s+=end($groupSpacing_mob); // add last defined groupSpacing
			}
		}
		return $s*$scaleSpacing;
	}
}else if($groupDirection == "vertical"){
	require_once("config/tiles.php");
	function getMarginLeft($group){
		return 0;
	}	
	function getMarginTop($group){
		global $scaleSpacing,$groupSpacing;
		$s=0;
		for($i=0;$i<$group;$i++){
			if(count($groupSpacing)>$i){ // if in array (to prevent errors);
				$s+=$groupSpacing[$i];
			}else{
				$s+=end($groupSpacing); // add last defined groupSpacing
			}
		}
		return $s*$scaleSpacing+45;
	}
}else{
	require_once("config/tiles.php");
	function getMarginLeft($group){
		global $scaleSpacing,$groupSpacing;
		$s=0;
		for($i=0;$i<$group;$i++){
			if(count($groupSpacing)>$i){ // if in array (to prevent errors);
				$s+=$groupSpacing[$i];
			}else{
				$s+=end($groupSpacing); // add last defined groupSpacing
			}
		}
		return $s*$scaleSpacing;
	}
	function getMarginTop($group){
		return 45;
	}
}
/* For DATA arguments */
function posVal($marginTop,$marginLeft,$width){
	echo " data-pos='".str_replace(".","_",$marginTop."-".$marginLeft.'-'.$width)."' ";
}

/* Generates tile titles  */
foreach($groupTitles as $l=>$title){
	?>
    <a href="#&amp;<?php echo strtolower(chars(str_replace(" ","-",$title)))?>" id="groupTitle<?php echo $l?>" class="groupTitle" style="margin-left:<?php echo getMarginLeft($l)?>px; margin-top:<?php echo getMarginTop($l)-45;?>px" onclick="javascript:$group.goTo(<?php echo $l?>);"><h3><?php echo $title?></h3></a>
    <?php
}

/* Generates tiles */
foreach($tile as $args){
	$n_args = array();
	foreach($tileTypes[$args['type']] as $key=>$std){
		if(array_key_exists($key,$args)){
			$n_args[] = $args[$key];
		}else{
			$n_args[] = $std;
		}
	}	
	call_user_func_array("tile_".$args['type'],$n_args);
}

?>