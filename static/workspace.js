
$(".overlay").click(function(){
	var file_id = $(this).attr("id")
	var form = document.createElement('form');
	form.setAttribute("method", "post");
	form.setAttribute("action", "/delete_file/"+file_id);
	form.setAttribute("id","delete-file");
	form.setAttribute("enctype","multipart/form-data");
	$("#delete-modal-body").append(form);
})

