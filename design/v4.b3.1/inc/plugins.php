<?php
$plugins = array();
function onEvent($event, $function){
	global $plugins;
	$plugins[$event][] = $function;
}
function triggerEvent($event){
	global $plugins;
	if(isset($plugins[$event])){
		foreach($plugins[$event] as $plugin){
			call_user_func($plugin);
		}
	}
}

$jsPluginsArray = array();
$cssPluginsArray = array();
?>