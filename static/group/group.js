function getMemberProfile(userPk, groupPk) {
	$.ajax({
		headers: {"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,}
		url: 'get/group-${groupPk}/user-${userPk}/profile',
		success: function(data) {
			container = document.getElementsByName('body')[0];
			container.innerHTML += data
		}
	})
}