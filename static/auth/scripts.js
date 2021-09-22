function loginPopUp(div, counter, email) {
	console.log("sb7")
	img = div.getElementsByTagName('img')[0].src
	modal = document.getElementsByClassName('modal')[counter-1]
	modal.style.display = 'block';
	emailInput = modal.getElementsByClassName('modal-content')[0].getElementsByTagName('form')[0].getElementsByTagName('input')[1]; 
	emailInput.value = email;
	emailInput.setAttribute('readonly', 'readonly')

	passInput = modal.getElementsByClassName('modal-content')[0].getElementsByTagName('form')[0].getElementsByTagName('input')[2]; 
	passInput.focus();
	modal.getElementsByTagName('img')[0].src = img

	span = modal.getElementsByClassName('modal-content')[0].getElementsByClassName('close')[0]
	span.onclick = function() {
		console.log("closed")
	  modal.style.display = "none";
	}

	window.onclick = function(event) {
	  if (event.target == modal) {
		modal.style.display = "none";
	  }
	}
} 

function loginFun(id) {
	form = $("#login-modal-" + id + "-form")
	var formData = form.serialize();
	$.ajax({
		headers: {
			"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
		},
		method: 'POST',
		data: formData,
		url: '/accounts/login/',
		success: function(message) {
			
			console.log(message)
			if (message.failure) {
				document.getElementById("login-modal-" + id + "-form").getElementsByTagName('input')[2].value = ''
				console.log("clear")
				document.getElementsByClassName('modal-alert')[parseInt(id-1)].style.display = 'block';
				
			} else {

				location.reload()
			}

		}

		
		}
	)
}