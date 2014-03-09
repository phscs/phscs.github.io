$(document).ready(function(){
	markdown();

	storeImageSizes();
	resizeImages();

	$(window).resize(function(){
		resizeImages();
	});
});

imageSizes = {};

function storeImageSizes(){
	$("img").each(function(index){
		img = $("img")[index];
		imageSizes[index] = {"width":img.width, "height":img.height};
	});
};

function resizeImages(){
	pageWidth = $("body").width();

	$("img").each(function(index){
		img = $("img")[index];
		imgRatio = imageSizes[index]["width"] / imageSizes[index]["height"];

		// restore to original size
		img.width = imageSizes[index]["width"];
		img.height = imageSizes[index]["height"];

		// shrink big images
		if (img.width > pageWidth){
			img.width = pageWidth;
			img.height = pageWidth / imgRatio;
		};
	});
};

function markdown(){
	text = $("body").html().split("");
	insideParagraph = false;
	insideHTMLTag = false;
	insideBlockCode = false;
	insideInlineCode = false;
	insideItalics = false;
	insideVocab = false;
	insideBold = false;
	tabsSinceNewLine = 0;
	newLinesSinceEnteringBlockCode = 0;

	// markup
	for (i=0; i<text.length; i++){
		character = text[i];

		if (character == "|"){
			insideBlockCode = !insideBlockCode;

			if (insideBlockCode){
				text[i] = "<div class='block-code'>";
			} else if (!insideBlockCode){
				text[i] = "</div>";
				newLinesSinceEnteringBlockCode = 0;
			};
		}

		else if (insideBlockCode){
			// watch out for closing pipes, all spaces (convert to non-breaking), all tabs (convert to four non-breaking spaces), newlines, and returns

			if (character == " "){
				text[i] = "&nbsp;";
			}

			else if (character == "\t"){
				tabsSinceNewLine += 1;

				if (tabsSinceNewLine > 1){
					text[i] = "&nbsp;&nbsp;&nbsp;&nbsp;";
				};
			}

			else if (character == "\n"){
				tabsSinceNewLine = 0;
				newLinesSinceEnteringBlockCode += 1;

				if (newLinesSinceEnteringBlockCode > 1){
					text[i] = "<br />";
				};
			};
		}

		else {
			// watch out for opening pipes, inline code, italics, vocab, bold, newlines, and returns
			if (character == "`"){
				insideInlineCode = !insideInlineCode;

				if (insideInlineCode){
					text[i] = "<span class='inline-code'>";
				} else if (!insideInlineCode){
					text[i] = "</span>";
				};
			}

			else if (character == "_" && !insideHTMLTag && !insideInlineCode && !insideBlockCode){
				insideItalics = !insideItalics;

				if (insideItalics){
					text[i] = "<i>";
				} else if (!insideItalics){
					text[i] = "</i>";
				};
			}

			else if (character == "~"){
				insideVocab = !insideVocab;

				if (insideVocab){
					text[i] = "<span class='vocab'>";
				} else if (!insideVocab){
					text[i] = "</span>";
				};
			}

			else if (character == "\n"){
				if (insideBlockCode && text[i-1] != "<div class='block-code'>"){
					text[i] = "<br />";
				} else if (
						text[i+1] == "\n" &&
						text[i-1] != ">" &&
						text[i+3] != "<" &&
						text[i-1] != "</div>" &&
						text[i+3] != "|"
					){
						text[i] = "<br />";
						text[i+1] = "<br />";
				};
			}

			else if (character == "<"){
				insideHTMLTag = true;
			}

			else if (character == ">"){
				insideHTMLTag = false;
			}

			else if (text.slice(i, i+4).join("") == " -- "){
				text[i] = "&#151;";
				text.splice(i+1, 3);
			}

			else if (text.slice(i, i+3).join("") == " - "){
				text[i] = "&#151;";
				text.splice(i+1, 2);
			};
		};
	};

	$("body").html(text.join(""));

	$("img").each(function(){
		$("<p>").insertBefore($(this));
		$("</p>").insertAfter($(this));
	});
};
