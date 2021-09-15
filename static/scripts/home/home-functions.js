function getPosts() {
	container = document.getElementsByClassName('posts-container')[0];
	counter = container.dataset.counter
	$.ajaxSetup({
		headers: {
			"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
		}
	});

	$.ajax({
		url: 'get/10-posts/' + counter,
		
		success: function(data) {
			container = document.getElementsByClassName('posts-container')[0];
			for (var i = 0; i < data.length; i++) {
				container.innerHTML += data[i]
			}
			container.setAttribute('data-counter', parseInt(counter) + data.length )
	}
})
}


$(window).scroll(function () {
	x = parseInt($(window).height()) + $(window).scrollTop() 
	y = parseInt($(document).height()) 
	if (x == y || x > y - 5) {
		console.log("bottom")
		getPosts()
	}
})

