$(document).ready(function(){
	syntaxHighlight();
});

function syntaxHighlight(){
	$(".python").each(function(index, data){
		text = $(data).html().split("");

		text = markComments(text);

		$(data).html(text.join(""));
	});
};

function markComments(text){
	// this function really accepts an array,
	// not a string!
	insideComment = false;
	insideSpecialComment = false;

	for (i=0; i<text.length; i++){
		character = text[i];

		if (text.slice(i, i+3).join("") == "###"){
			insideSpecialComment = true;
			text[i] = "<span class='python_comment_special'>";
			text.splice(i+2, 1);
		} else if (character == "#" && !insideSpecialComment){
			insideComment = true;
			text[i] = "<span class='python_comment'>" + character;
		} else if (
						text.slice(i, i+6).join("") == "<br />" ||
						text.slice(i, i+5).join("") == "<br/>" ||
						text.slice(i, i+4).join("") == "<br>" ||
						character == "\n"
				  ){
						insideComment = false;
						insideSpecialComment = false;
						text[i] = "</span>" + character;
				  }
	};
	
	return text;
}
