$(window).resize(function(){
	$("#admin-editor, #contentWrapper").height($(window).height()-$("#admin-headerWrapper").height()-1);
	editor.resize();
});


$(document).on("click","#saveButton",function(){
		$("#msgbox").removeClass().addClass('messagebox').text('Validating....').fadeIn(1000);
		$.post('ajax_saveFile.php',
		{content:editor.getValue(),file:file},
		function(data){
			if(data=='yes') {
				var currentTime = new Date()
				var hour = currentTime.getHours()
				var minute = currentTime.getMinutes()
	           	$("#msgbox").fadeTo(300,0.1,function(){
	               	$(this).html('Saved @ '+hour+':'+minute).addClass('messageboxok').fadeTo(900,1);
	           	});
	       	}else{
	            $("#msgbox").fadeTo(300,0.1,function(){
	           	    $(this).html(data).addClass('messageboxerror').fadeTo(900,1);
	       	    });
	       	}
		});	
});
$(document).on("click","#deleteButton",function(){
		if(confirm("Are you sure you want to delete this file? For safety reasons, the file will be moved to /admin/trash/ ")){
			$("#msgbox").removeClass().addClass('messagebox').text('Validating....').fadeIn(1000);
			$.post('ajax_deleteFile.php',
			{file:file},
			function(data){
				if(data=='yes') {
		           	$("#msgbox").fadeTo(300,0.1,function(){
		               	$(this).html('Deleted!').addClass('messageboxok').fadeTo(900,1);
						alert("File moved to /admin/trash/ ");
						window.location.href="home.php";
		           	});
		       	}else{
		            $("#msgbox").fadeTo(300,0.1,function(){
		           	    $(this).html(data).addClass('messageboxerror').fadeTo(900,1);
		       	    });
		       	}
			});	
		}
});
