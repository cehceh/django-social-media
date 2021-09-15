modals = document.getElementsByClassName('GroupProfileModal')

for (var i = modals.length - 1; i >= 0; i--) {
	modals[i].addEventListener('click', function() {
		modal.remove()
	})
}