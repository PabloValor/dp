<?php
$tileTypes['flipText'] = array( /* Defaults*/
	"group"=>0,
	"x"=>0,
	"y"=>0,
	'width'=>1,
	'height'=>1,
	"background"=>$defaultBackgroundColor,
	"backgroundHover"=>"",
	"url"=>"",
	"title"=>"Text on the front",
	"text"=>"Your text for the backside",
	"direction"=>"vertical", // vertical or horizontal
	"img"=>"","imgAlt"=>"","imgTitle"=>"",
	"imgSize"=>"50",
	"imgToTop"=>"0",
	"imgToLeft"=>"0",
	"labelText"=>"",
	"labelColor"=>$defaultLabelColor,
	"labelPosition"=>$defaultLabelPosition,
	"classes"=>"",
);
function tile_flipText($group,$x,$y,$width,$height,$background,$backgroundHover,$url,$title,$text,$direction,$img,$imgAlt,$imgTitle,$imgSize,$imgToTop,$imgToLeft,$labelText,$labelColor,$labelPosition,$classes){
	global $scale, $spacing, $scaleSpacing, $groupSpacing;
	
	$marginTop = $y*$scaleSpacing+getMarginTop($group);
	$marginLeft = $x*$scaleSpacing+getMarginLeft($group);
	$tileWidth = $width*$scaleSpacing-$spacing;
	$tileHeight = $height*$scaleSpacing-$spacing;
	?>
  	<a <?php echo makeLink($url);?> class="tile tileFlipText <?php echo $direction;?> group<?php echo $group?> <?php echo $classes?>" style="
    margin-top:<?php echo $marginTop?>px; margin-left:<?php echo $marginLeft?>px;
	width:<?php echo $tileWidth?>px; height:<?php echo $tileHeight;?>px;" <?php posVal($marginTop,$marginLeft,$tileWidth);?>> 
    

    <div class='flipContainer'>
		<div class='flipFront' style="background:<?php echo $background;?>;">
		<?php 
		if($labelText!=""){
			if($labelPosition=='top'){
				echo "<div class='tileLabelWrapper top' style='border-top-color:".$labelColor.";'><div class='tileLabel top' >".$labelText."</div></div>";
			}else{
				echo "<div class='tileLabelWrapper bottom'><div class='tileLabel bottom' style='border-bottom-color:".$labelColor.";'>".$labelText."</div></div>";
			}
		}
		?>
		<h3>
		<?php if($img != ""){?>
    	<img title='<?php echo $imgTitle?>' alt='<?php echo $imgAlt?>' style='margin-top:<?php echo $imgToTop?>px;margin-left:<?php echo $imgToLeft?>px;' 
    	src='<?php echo $img?>' height="<?php echo $imgSize?>" width="<?php echo $imgSize?>"/>
    	<?php }?>
    	<?php echo $title?>
    	</h3></div>
		<div class='flipBack' style="background:
		<?php
		if($backgroundHover==""){
			echo $background;
		}else{
			echo $backgroundHover;
		}
		?>;"><h5><?php echo $text?></h5></div>
        
	</div>
    </a>
    <?php
}
?>