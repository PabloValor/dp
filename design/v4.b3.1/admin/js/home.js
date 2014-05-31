$(document).ready(function(){
	$("#newPage").click(function(){
		$(this).hide(500);
		$("#newPageWrapper").show(500);
	});
	$("#newPageSubmit").click(function(){
		$("#newPageMsgbox").removeClass().addClass('messagebox').text('Validating....').fadeIn(1000);
		newPageName = $('#newPageName').val();
		$.post('ajax_newPage.php',
		{name:newPageName},
		function(data){
			if(data=='yes') {
	           	$("#newPageMsgbox").fadeTo(300,0.1,function(){
	               	$(this).html('Page created!').addClass('messageboxok').fadeTo(900,1);
					window.location.reload();
	           	});
	         }else{
	            $("#newPageMsgbox").fadeTo(300,0.1,function(){
	                $(this).html(data).addClass('messageboxerror').fadeTo(900,1);
	           });
	       	}
		});		
	});
	$("#goPathForm").submit(function(){
		window.location.href = "code-editor.php?p=../"+$("#goPathLink").val();
		return false;
	});
	$("#flushCacheButton").click(function(){
		$("#flushMsgbox").removeClass().addClass('messagebox').text('Flushing...').fadeIn(1000);
		$.post('ajax_flushCache.php',
		function(data){
			if(data=='yes') {
	           	$("#flushMsgbox").fadeTo(300,0.1,function(){
	               	$(this).html('Cache flushed!').addClass('messageboxok').fadeTo(900,1);
					if(confirm("NoJS file is removed, click OK to go to your mobile site and rebuild the cache. If you do not do this, this can be a potential security leak.")){
						window.location.href='../mobile.php'
					}
	           	});
	         }else{
	            $("#flushMsgbox").fadeTo(300,0.1,function(){
	                $(this).html(data).addClass('messageboxerror').fadeTo(900,1);
	           });
	       	}
		});	
	});
	$(".plugindirs").click(function(){
		 $("#pluginlink"+$(this).attr("id").substr(9)).toggle();
		 return false;
	});
	$(".themedirs").click(function(){
		 $("#themelink"+$(this).attr("id").substr(8)).toggle();
		 return false;
	});
});