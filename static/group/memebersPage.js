const membersPage = document.getElementById('members-container').innerHTML
input = document.getElementById('Members-Search-Input')
container = document.getElementById('members-container')
input.addEventListener('input', function() {
	var changed = false
	if (! this.value.length ==- 0) {
		$.ajax({
			method: 'GET',
			'headers': {"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,},
			url: '/get/group/number/' + this.dataset.pk + '/members/',
			data: {'searched': this.value},
			success: function(data) {
				if (data.Found) {
					alert("not found")
				} else {
					if (changed == false) {
						changed = true
						container.innerHTML = ''
						for (var i = data.length - 1; i >= 0; i--) {
							container.innerHTML += data[i]
						}
					}

				}
				
			} 
		})
	} else {
		container.innerHTML = membersPage
	}
})

input.addEventListener('change', function() {
	console.log(this.value.length)
	if (this.value.length === 0) {
		container.innerHTML = membersPage
	}
})

input.addEventListener('search', function() {
	console.log(this.value.length)
	if (this.value.length === 0) {
		container.innerHTML = membersPage
	}
})