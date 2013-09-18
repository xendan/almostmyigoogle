function visited(id, visited) {
	$.post( "/visited/", {id: id, visited:visited});
}

function unvisited(id) {
	visited(id, false);
	$(".fancybox-close")[0].click();
	return false;
}
$(
	function() {
		var page = 1;

		function showMessage(isError, message) {
			if (isError) {
				console.error(message);
			} else {
				console.log(message);
			}
		}
	
		function onItemClick(item, li) {
			visited(item.id, true)
			var p = "<p><a href='#' onclick='unvisited(" + item.id + ")'>Read later</a>" + originalLink(item) + "</p>";
			$.fancybox({ content: item.content + p });
			$(li).addClass("visited");
			return false;
		}	

		function scrollItem(moveDown) {
			var first = $("#items").find("li:first");
			$("#items li").each(function() {
				if ($(this).offset().top > 0) {
					first = $(this);
					return false;	
				}
			});
			var scrollTo = moveDown ? first.next() : first.prev();
			if (scrollTo.length) {
				var container = $("#wrapper");
				container.animate({
  					scrollTop: scrollTo.offset().top - container.offset().top + container.scrollTop()
				});
			}
			if (moveDown) {
				var loading =  $("#loading");
				if (loading.length > 0 && 
					loading.offset().top <= $("#arrow_down").offset().top) {
					page++;
					loadItems();
					
				}
			}
			return false;
		}
		
		function loadItems() {
			var cat = "";
			$("#categories option:selected").each(function() {
      				cat += $( this ).val();
    			});
			$.getJSON("/lookup/", {category:cat, page:page}, function(json){
				$("#loading").remove();
				if (json['error']) {
					showMessage(true, json['error']);
				} else {
					$.each(json['items'], addItem);
				}
				if (page < json['num_pages']) {
					$("#items").append("<li id='loading'>Loading...</li>");
				}
			});
		}

		function onCategoryChange() {
			page = 1;
			$("#items").empty();
			loadItems();
  		}

		function originalLink(item) {
			return "<a href='" + item.link+ "' >" 
				+ item.entry_title
				+ "</a>"
		}

		function addItem(index, item) {
			var li = document.createElement('li');
			var a = document.createElement('a');
			$(a).html(item.title);
			$(a).click(function(){
				onItemClick(item, li);
			})
			$(li).append(a).append(
				"<div>" + originalLink(item) +"</div>");
			$("#items").append(li);
		}
		$('#categories').change(onCategoryChange);
		onCategoryChange();
		$("#arrow_up").click(function(){scrollItem(false)});
		$("#arrow_down").click(function(){scrollItem(true)});
	}
);
