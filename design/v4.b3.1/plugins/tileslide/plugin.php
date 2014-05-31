<?php
$tileTypes['slide'] = array( /* Defaults*/
	"group"=>0,
	"x"=>0,
	"y"=>0,
	'width'=>2,
	'height'=>1,
	"background"=>$defaultBackgroundColor,
	"url"=>"",
	"text"=>"Hovered text",
	"img"=>"",
	"imgAlt"=>"",
	"imgTitle"=>"",
	"imgSize"=>1.0,
	"slidePercent"=>0.40,
	"slideDir"=>"up",
	"doSlideText"=>true,
	"doSlideLabel"=>true,
	"border"=>false,
	"labelText"=>"",
	"labelColor"=>$defaultLabelColor,
	"labelPosition"=>$defaultLabelPosition,
	"classes"=>"",
);
function tile_slide($group,$x,$y,$width,$height,$background,$url,$text,$img,$imgAlt,$imgTitle,$imgSize,$slidePercent,$slideDir,$doSlideText,$doSlideLabel,$border,$labelText,$labelColor,$labelPosition,$classes){
	global $scale, $spacing, $scaleSpacing, $groupSpacing;
	$tileWidth = $width*$scaleSpacing-$spacing;
	$tileHeight = $height*$scaleSpacing-$spacing;
	$marginTop = $y*$scaleSpacing+getMarginTop($group);
	$marginLeft = $x*$scaleSpacing+getMarginLeft($group);
	switch($slideDir){
		case "left":
		case "right":$d = 'hor';break;
		case "down":
		case "up": $d = 'ver';break;
	}
	?>
  	<a <?php echo makeLink($url);?> class="tile tileSlide <?php echo $slideDir?> group<?php echo $group?> <?php echo $classes?>" style="
    margin-top:<?php echo $marginTop;?>px; margin-left:<?php echo $marginLeft?>px;
	width:<?php echo $tileWidth?>px; height:<?php echo $tileHeight?>px;
	background:<?php echo $background;?>; <?php if(!$border){echo "padding:0;";}?>" <?php posVal($marginTop,$marginLeft,$tileWidth);?> data-doslide="<?php echo $doSlideText;?>"> 
    
    
    <div class='slideText' style='
    <?php 
	if($d == "ver"){?>
        height:<?php echo $tileHeight*$slidePercent?>px; width:100%;<?php
	}else{?>
    	width:<?php echo $tileWidth*$slidePercent?>px; height:100%;<?php
	} 
	if($doSlideText){
		switch($slideDir){
			case "left": echo "left:".$tileWidth.'px;';break;
			case "right":echo "left:".-$tileWidth*$slidePercent.'px;';break;
			case "down":echo "top:".-$tileHeight*$slidePercent.'px;';break;
			case "up": echo "top:".$tileHeight.'px;';break;
		}
	}else{
		switch($slideDir){
			case "left": echo "right";break;
			case "right":echo "left";break;
			case "down":echo "top";break;
			case "up": echo "bottom";break;
		}
		echo ":0;";
	}
	?>
    '>
    <?php
    echo $text;
	?>
    </div>
    <div class="imageWrapper">
    	<div class="imageCenterer" style="width:<?php echo $tileWidth?>px; height:<?php echo $tileHeight?>px;line-height:<?php echo $tileHeight-2?>px;">
			<img src='<?php echo $img;?>' alt="<?php echo $imgAlt?>" title="<?php echo $imgTitle?>" style="width:<?php echo $tileWidth*$imgSize;?>px;" /> 
        </div>
		<?php 
		if(!$doSlideLabel){
			echo "</div>";
		}
		if($labelText!=""){
			if($labelPosition=='top'){
				echo "<div class='tileLabelWrapper top' style='border-top-color:".$labelColor.";'><div class='tileLabel top' >".$labelText."</div></div>";
			}else{
				echo "<div class='tileLabelWrapper bottom'><div class='tileLabel bottom' style='border-bottom-color:".$labelColor.";'>".$labelText."</div></div>";
			}
		}
		if($doSlideLabel){
			echo "</div>";
		}
		?> 
   
    </a>
    <?php
}
?>