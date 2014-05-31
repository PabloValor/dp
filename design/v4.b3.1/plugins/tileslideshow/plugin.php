<?php
$tileTypes['slideshow'] = array( /* Defaults*/
	"group"=>0,
	"x"=>0,
	"y"=>0,
	'width'=>2,
	'height'=>1,
	"background"=>$defaultBackgroundColor,
	"url"=>"",
	"images"=>array(),
	"alts"=>array(),
	"texts"=>array(),
	"effect"=>"slide-right",
	"speed"=>6000,
	"arrows"=>true,
	"labelText"=>"",
	"labelColor"=>$defaultLabelColor,
	"labelPosition"=>$defaultLabelPosition,
	"classes"=>"",
);
function tile_slideshow($group,$x,$y,$width,$height,$background,$url,$images,$alts,$texts,$effect,$speed,$arrows,$labelText,$labelColor,$labelPosition,$classes){
	global $scale, $spacing, $scaleSpacing, $groupSpacing;
	$id =  str_replace(".","_",$group."-".$x."-".$y);
	$tileWidth = $width*$scaleSpacing-$spacing;
	$tileHeight = $height*$scaleSpacing-$spacing;
	$marginTop = $y*$scaleSpacing+getMarginTop($group);
	$marginLeft = $x*$scaleSpacing+getMarginLeft($group);
	if(count($alts)!=count($images)) $alts = array_fill(count($alts), count($images)-count($alts), "");
	?>
  	<a <?php echo makeLink($url);?> id="tileSlideshow<?php echo $id?>" class="tile tileSlideshow group<?php echo $group?> <?php echo $classes?>" style="
    margin-top:<?php echo $marginTop;?>px; margin-left:<?php echo $marginLeft?>px;
	width:<?php echo $tileWidth?>px; height:<?php echo $tileHeight?>px;
	background:<?php echo $background;?>;" <?php posVal($marginTop,$marginLeft,$tileWidth);?> data-n=0> 
    
    <div class='imgWrapperBack' style="width: <?php echo $tileWidth+2?>px; height:<?php echo $tileHeight+2?>px"><img src='<?php echo $images[0]?>' alt=''/></div>
	<div class='imgWrapper' style="width: <?php echo $tileWidth+2?>px; height:<?php echo $tileHeight+2?>px"><img src='<?php echo $images[0]?>' alt='<?php echo $alts[0]?>' /></div>
   
    <?php
	if($texts != "" && count($texts)>0){
		echo  "<div class='imgText'>".$texts[0]."</div>";
	}
	?>
   
    <script>slideshowTiles["tileSlideshow<?php echo $id?>"] = [<?php echo json_encode($images)?>,<?php echo json_encode($alts);?>,<?php echo json_encode($texts);?>,<?php echo '"'.$effect.'"';?>,<?php echo $speed?>]</script>
    
    <?php
	if($arrows){
		echo '<img id="sl_arrowRight" src="img/arrows/simpleArrowRight.png" alt="Slideshow - right"><img id="sl_arrowLeft" src="img/arrows/simpleArrowLeft.png" alt="Slideshow - left">';
	}
	if($labelText!=""){
		if($labelPosition=='top'){
			echo "<div class='tileLabelWrapper top' style='border-top-color:".$labelColor.";'><div class='tileLabel top' >".$labelText."</div></div>";
		}else{
			echo "<div class='tileLabelWrapper bottom'><div class='tileLabel bottom' style='border-bottom-color:".$labelColor.";'>".$labelText."</div></div>";
		}
	}
	?> 
    </a>
    <?php
}
?>