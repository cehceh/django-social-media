
function getMemberProfile(userPk, groupPk) {
	$.ajax({
		headers: {"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,},
		url: 'get/group-${groupPk}/user-${userPk}/profile',
		success: function(data) {
			container = document.getElementsByName('body')[0];
			container.innerHTML += data
		}
	})
}

function getGroupPosts() {
	container = document.getElementsByClassName('group-posts-container')[0];
	counter = container.dataset.counter
	pk = container.dataset.id
	$.ajaxSetup({
		headers: {
			"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
		}
	});

	$.ajax({
		url: '/get/group/10-posts/',
		data: {'pk':pk, 'counter':counter},
		method: 'POST',
		success: function(data) {
			container = document.getElementsByClassName('group-posts-container')[0];
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
		getGroupPosts()
	}
})

function InviteMember(btn, group, user){
	$.ajax({
		url: '/invite/group/member/',
		data: {'groupPK':group, 'userPK':user},
		method: 'POST',
		success: function(data) {
			if (data.success == true) {
				btn.innerHTML = 'Invited'
			} else {
				alert("something went wrong please try again later")
			}
		}
	})
}

