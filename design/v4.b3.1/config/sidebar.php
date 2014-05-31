<?php
$sidebar["an_example"] = array("pos"=>"left","size"=>2,"full_height"=>false/*<- this sets wether the sidebar should be the full page height or not*/,
	"tiles"=>array( /* Open the array of sidebar tiles */
	
 array("type"=>"custom","group"=>0,"x"=>0,"y"=>0,'width'=>1,'height'=>1,"background"=>"#11528f","url"=>"typography.php",
"content"=>
"<div style='line-height:30px; margin-top:5px;'>
<div style='color:#FFF;font-size:43px;line-heigt:70px;'><strong>CHECK</strong></div>
<span style='color:#FFF;font-size:32px;'><strong>OUT</strong></span><span style='color:#BBB;font-size:32px;'>THE</span>
<div style='font-size:57px;line-height:30px;'>TYPO</div>
<div style='font-size:37px;line-height:40px;'>GRAPHY</div>
</div>"),

array("type"=>"img","group"=>0,"x"=>1,"y"=>0,'width'=>1,'height'=>1,"background"=>"#0F6D32","url"=>"",
	"img"=>"img/img3.jpg","desc"=>"By adding the CSS class 'noClock' to this tile, we've achieved that there is no hover effect!",
	"showDescAlways"=>true,"imgWidth"=>1,"imgHeight"=>1,
	"labelText"=>"Img Tile","labelColor"=>"#509601","labelPosition"=>"bottom", "classes"=>"noClick"),

	), /* Close the array of sidebar tiles */
	"load_plugins"=>array() /* Load plugins from the plugin folder so you can use tileplugins */
);


$sidebar["some_info"] = array("pos"=>"left","size"=>2,"full_height"=>true/*<- this sets wether the sidebar should be the full page height or not*/,
	
	"tiles"=>array( /* Open the array of sidebar tiles */
		
		array("type"=>"simple","group"=>0,"x"=>0,"y"=>0,'width'=>1,'height'=>1,"background"=>"#509601","url"=>"#","title"=>"Home","text"=>"Return to homepage"),
		
		array("type"=>"flip","group"=>0,"x"=>1,"y"=>0,'width'=>1,'height'=>1,"background"=>"#C82345","url"=>"","img"=>"img/metro_150x150.png",
	"text"=>"<h4 style='color:#FFF;margin-top:10px;' >Even plugins can work in sidebars!</h4>", "classes"=>"noClick"),
		
		array("type"=>"slide","group"=>0,"x"=>0,"y"=>1,'width'=>2,'height'=>1,"background"=>"#00BFFF","url"=>"accordions.php",
	"text"=>"<h3>Check the accordions</h3>","img"=>"img/metro_slide_300x150_2.png","imgSize"=>1,
	"slidePercent"=>0.40,
	"slideDir"=>"up", // can be up, down, left or right
	"doSlideText"=>true,"doSlideLabel"=>true,
	"labelText"=>"Accordions","labelColor"=>"#00BFFF","labelPosition"=>"top",),
	
	), /* Close the array of sidebar tiles */
	
	"load_plugins"=>array("tileflip","tileslide") /* Load plugins from the plugin folder so you can use tileplugins */
);