 function previewContent(){
	$("#content").html($("<div>"+editor.getValue()+"</div>").find("script").remove().end().html());
	
	$("#content").find("img").each(function(){
		var src= $(this).attr("src")
		if(src.substr(0,6) != "http://" && src.substr(0,7) != "https://"){
			if($(this).attr("src")[0] == "/"){
				$(this).attr("src",".."+src);
			}else{
				$(this).attr("src","../"+src);
			}
		}
	})
}
$(document).ready(function(){
	editor = ace.edit("admin-editor");
    editor.setTheme("ace/theme/textmate");
    editor.getSession().setMode("ace/mode/html");
	$(window).resize();
	
	$("#leftWidth").keyup(function(){
		var val = $(this).val();
		if(val != "" && parseInt(val) != val){
			$(this).val(40);
		}
		if($(this).val()>100){
			$(this).val(90);
		}
		if($(this).val()<0){
			$(this).val(10)
		}
		$("#admin-editor").width(val+"%");
		editor.resize();
		$("#contentWrapper").width((100-val)+"%");
	});
	$("#previewNow, #enableLive").click(function(){
		previewContent();
	});
	
	previewContent();
	
	
	editor.getSession().on('change', function(e) {
		if($('#enableLive').is(':checked')){
			previewContent();
		}
	});
	
	
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

$(window).resize(function(){
	$("#admin-editor, #contentWrapper").height($(window).height()-$("#admin-headerWrapper").height());
	editor.resize();
});
