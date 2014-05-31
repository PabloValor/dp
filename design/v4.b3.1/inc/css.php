<style>
<?php 
if($font != ""){
	?>
	html{
		font-family: <?php echo $font?>;
	}
	<?php
}
?>
html{background-color:<?php echo $bgColor?>;}

<?php
if($bgImage!="" ){?>
		#bgImage { position:fixed; top:0; left:0; z-index:-4; min-width:<?php echo $bgWidth?>%;min-height:100%;
		<?php if($bgMaxScroll != 0){?>
			-webkit-transition:margin-left <?php echo $bgScrollSpeed?>ms linear;
			-moz-transition:margin-left <?php echo $bgScrollSpeed?>ms linear;
			-o-transition:margin-left <?php echo $bgScrollSpeed?>ms;
			-ms-transition:margin-left <?php echo $bgScrollSpeed?>ms;
			transition:margin-left <?php echo $bgScrollSpeed?>ms;
			<?php } ?>
		}
		<?php
}
?>
<?php if($autoRearrangeEffect){?>
	.tile{
	-webkit-transition-property: box-shadow, margin-left,  margin-top;
	-webkit-transition-duration: 0.25s, 0.5s, 0.5s;
	-moztransition-property: box-shadow, margin-left,  margin-top;
	-moz-transition-duration: 0.25s, 0.5s, 0.5s;
	-o-transition-property: box-shadow, margin-left,  margin-top;
	-o-transition-duration: 0.25s, 0.5s, 0.5s;
	-ms-transition-property: box-shadow, margin-left,  margin-top;
	-ms-transition-duration: 0.25s, 0.5s, 0.5s;
	transition-property: box-shadow, margin-left,  margin-top;
	transition-duration: 0.25s, 0.5s, 0.5s;
	}
<?php 
}
if($groupDirection == "vertical" && $scrollHeader == true){
	?>
	.full>header{
		position:absolute;
	}
	<?php
}
if(!$scrollHeader){?>
	#subNavWrapper{
	    position:fixed;
	    right:0;
	    left:0;
	}
	#centerWrapper{
	    margin-top:40px;
	}
<?php
}
if($maxPageWidth != "900"){
	?>
#headerCenter{
	max-width:<?php echo $maxPageWidth?>px;
}
#centerWrapper{
	max-width:<?php echo $maxPageWidth?>px; /* MAX WIDTH OF PAGE*/
}
	<?php
}
if(isset($_SESSION['username']) && $_SESSION['username'] == $username){
	?>
#adminPanel{
	position:fixed;
	bottom:0;
	left:0;
}
#adminText{
	background-color:#668800;
	padding:3px;
	color:#FFF;
	text-decoration:none;
}
#adminText:hover{
	background-color:#678000;
	text-decoration:underline;
}
#adminHovered{
	display:none;
	list-style:none;
	margin:0;
	background-color:#333;
	color:#FFF;
	margin-bottom:3px;
}
#adminHovered>li>a{
	color:#FFF;
	text-decoration:none;
	display:block;
	padding:3px;
}
#adminHovered>li>a:hover{
	text-decoration:underline;
}
#adminPanel:hover #adminHovered{
	display:block;
}
	<?php
}
?>
</style>