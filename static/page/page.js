function getPagePosts() {
	container = document.getElementsByClassName('modal-posts-container')[0];
	counter = container.dataset.counter
	pk = container.dataset.id
	$.ajaxSetup({
		headers: {
			"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
		}
	});

	$.ajax({
		url: '/get/page/10-posts/',
		data: {'pk':pk, 'counter':counter},
		method: 'POST',
		success: function(data) {
			container = document.getElementsByClassName('modal-posts-container')[0];
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
		getPagePosts()
	}
})
