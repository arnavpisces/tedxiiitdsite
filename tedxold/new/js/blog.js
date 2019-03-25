function showfullblog(element) {
	$(".blog-content-all").slideUp();
	$(".blog-content-small").slideDown();
	idsmall = "#" + element + "small";
	idall = "#" + element + "all";
	$(".blog-content-all").closest("div").css("border-left", "5px solid #bbb");
	if ($(idall).css("display") == "none") {
		$(idsmall).fadeOut(400, function() {
			$(idall).slideDown();
			$(idsmall).closest("div").css("border-left", "5px solid #3B5998");
		});
	}
}