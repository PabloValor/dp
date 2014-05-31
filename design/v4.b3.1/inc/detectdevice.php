<?php
/*Device detection */
include_once('inc/mobile_device.php');

if($enableMobile){
	if ($redirectPhone && $device=="mobile"  && ((!$redirectTablet  && $device!="tablet") || ($redirectTablet && $device=="tablet"))){ //Redirect if needed, according to settings
		if(!isset($_COOKIE['fullsite']) || $_COOKIE['fullsite'] != 1){
			header("Location: mobile.php");
		}else{
			$device = "mobileOnDesktop";
		}
	}
}
$mobile = false;
?>