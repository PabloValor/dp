<?php
/*Include necessary files*/
include_once("inc/plugins.php");
include_once("inc/defaults.php");
include("config/general.php");
include("config/layout.php");
include("config/pages.php");
include_once("inc/init.php");
include_once("inc/tilefunctions.php");

$sidebar = array();
/*Init tile functions if not inited yet */

if(!function_exists("getMarginLeft")){
	function getMarginLeft($group){
		return 0;
	}
}
if(!function_exists("getMarginTop")){
	function getMarginTop($group){
		return 0;
	}
}
if(!function_exists("posVal")){
	function posVal($marginTop,$marginLeft,$width){
		echo " ";
	}
}
function showSidebar($name){
	global $sidebar,$scale, $spacing, $scaleSpacing, $groupSpacing,$tileTypes, $defaultBackgroundColor, $defaultLabelColor, $defaultLabelPosition;
	include_once("config/sidebar.php");
	if(!array_key_exists($name,$sidebar)){ // if sidebar not found
		echo "Sidebar could not be loaded because sidebar name doesn't exist";
	}else{
		$t = $scaleSpacing*$sidebar[$name]['size']+5; // width of sidebar
		?>
        <div class='sidebar sidebar-<?php echo $name;?> sidebar-<?php echo $sidebar[$name]['pos']?>' <?php if($sidebar[$name]['pos']!="top"){?>style='width:<?php echo $t?>px'<?php } ?>>
        <?php
		triggerEvent("sidebarBegin");
		/* Plugins */
		foreach($sidebar[$name]["load_plugins"] as $plugin){
			if(file_exists("../plugins/".$plugin."/plugin.php")){
				include_once("plugins/".$plugin."/plugin.php");
			}
		}
		/* Load tiles */
		foreach($sidebar[$name]["tiles"] as $args){
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
		triggerEvent("sidebarEnd");
		?>
        </div>
        <style>
		<?php
		switch($sidebar[$name]["pos"]){
			case "left":
			if($sidebar[$name]["full_height"]){
				echo "#content{margin-left:".$t."px;}.sidebar-".$name."{margin-left:-".$t."px;}";
			}else{
				echo "#content{margin-left:0px;}.sidebar-left{margin-left:0px;}";
			}
			break;
			case "right":
			if($sidebar[$name]["full_height"]){
				echo "#content{margin-right:".$t."px;}.sidebar-".$name."{margin-right:-".$t."px;}";
			}else{
				echo "#content{margin-right:0px;}.sidebar-".$name."{margin-right:0px;}";
			}
			break;
		}
		?>
		</style>
        <noscript>
        <style>.sidebar>*{position:relative;top:0;margin:5px !important;display:inline-block;}</style>
        </noscript>
        <script>
		/* Fix height of sidebar for layout */
		sbDown = 0;
	    $("#content, #panelContent").children('.sidebar').children(".tile").each(function(){
			if(typeof $(this).attr("href") != "undefined"){
				$(this).attr("href",$(this).attr("href").replace("?p=","#!/"));
			}	
			var thisDown= parseInt($(this).css("margin-top"))+$(this).height();
			if(thisDown>sbDown){
				sbDown=thisDown;
			}	
		});
		$('#contentWrapper, .sidebar').css("min-height",sbDown+20+"px");
		
		
		/* Responsive sidebar position */
		<?php if($sidebar[$name]["pos"] != "top"){?>
		<?php if($sidebar[$name]["pos"] == "left"){
			  if($sidebar[$name]["full_height"]){?>
		$.plugin($toColumn,{
			sidebarAfter:function(){
				$("#content").children(".sidebar").appendTo("#centerWrapper").css("top",20).css("margin-left",0);
				$("#content").css("margin-left",0);
			}
		});
		$.plugin($toSmall,{
			sidebarBefore:function(){
				$("#centerWrapper").children(".sidebar").prependTo("#content").css("top",0).css("margin-left",-$(".sidebar").width());
				$("#content").css("margin-left",$(".sidebar").css("width"));
			}
		}); 
		<?php }else{?>
		$.plugin($toColumn,{
			sidebarAfter:function(){
				$("#content").children(".sidebar").appendTo("#centerWrapper").css("top",20).css("margin-left",0);
			}
		});
		$.plugin($toSmall,{
			sidebarBefore:function(){
				$("#centerWrapper").children(".sidebar").prependTo("#content").css("top",0).css("margin-left",$(".sidebar").css("width"));
			}
		}); 
		<?php }
		}else{
			if($sidebar[$name]["full_height"]){?>
			$.plugin($toColumn,{
				sidebarAfter:function(){
					$("#content").children(".sidebar").appendTo("#centerWrapper").css("top",20).css("left",-$(".sidebar").width());
					$("#content").css("margin-right",0);
				}
			});
			$.plugin($toSmall,{
				sidebarBefore:function(){
					$("#centerWrapper").children(".sidebar").prependTo("#content").css("top",0).css("left",0);
					$("#content").css("margin-right",$(".sidebar").width());
				}
			}); 
			<?php
			}else{?>
			$.plugin($toColumn,{
				sidebarAfter:function(){
					$("#content").children(".sidebar").appendTo("#centerWrapper").css("top",20)
				}
			});
			$.plugin($toSmall,{
				sidebarBefore:function(){
					$("#centerWrapper").children(".sidebar").prependTo("#content").css("top",0)
				}
			}); 
			<?php
			}
		}
		?>
		$.plugin($toFull,{
			sidebarBefore:function(){
				$toSmall.sidebarBefore();
			}
		});
		$.plugin($beforeSubPageShow,{
			checkSidebar:function(){
				switch($page.layout){
					case "column": $toColumn.sidebarAfter();break;
					case "small": $toSmall.sidebarBefore();break;
					case "full": $toSmall.sidebarBefore();break;
				}
			}
		});
		<?php }?>
		$events.sidebarShow();
		</script>
        <?php
	}
}
?>