input = document.getElementById('Members-Search-Input')
container = document.getElementById('members-container')
input.addEventListener('input', function() {
	var changed = false
	if (/\S/.test(this.value)) {
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
	}
})

input.addEventListener('change', function() {
	console.log(this.value.length)
	if (this.value.length === 0) {
		console.log("ajaxing")
		$.ajax({
			method: 'GET',
			'headers': {"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,},
			url: '/group-' + this.dataset.pk + '/members',
			data: {'searched': this.value},
			success: function(data) {
					container.innerHTML = data

				
			} 
		})
	}
})