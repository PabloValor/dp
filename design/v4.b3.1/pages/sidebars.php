<?php
$subNav = array(
	"Welcome ; welcome.php ; #509601;",
	"Accordions ; accordions.php ; #509601;",
	"Sidebars ; sidebars.php ; #509601;",
);


set_include_path("../");
include_once("inc/essentials.php");

/*Include a sidebar */
include_once("inc/sidebar.php");
showSidebar("some_info");
?>

<script>
$mainNav.set("tilegroup 2")
</script>


<h1 class="margin-t-0">Sidebars</h1>
<hr>
<p>This page will have a sidebar on the left.
<p>Did you know we can have a sidebar in a sidepanel? Click <a href="panels/example.php">here</a> to see the example.
<p>By the way, you can link to any metro page using the method like this (check source): <a <?php metroLink("welcome.php")?>>Link to welcome page</a>.
<p>If you prefer to open it in a new tab, you can do that this way: <a <?php metroLink("newtab:welcome.php")?>>Link to new tab</a>.
<p>Easy, isn't it?