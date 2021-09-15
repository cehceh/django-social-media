dummy = document.getElementsByClassName('dummy-request');
function AcceptUserRequestToGroup(x,y) {
	$.ajax({
		headers: {"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,},
		url: '/accept/user/group/join/request/',
		method: 'POST',
		data: {'group':x, 'user':y,},
		success : function(data) {
			document.getElementById('request-container-'+y).remove()
			if (dummy.length == 0) {
				document.getElementById('requests-container').innerHTML = "<h1 style='text-align:center;'> No more requests </h1>"
			}
		}
	})
}

function DenyUserRequestToGroup(x,y) {
	$.ajax({
		headers:  {"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,},
		url: '/deny/user/group/join/request/',
		method: 'POST',
		data: {'group':x, 'user':y,},
		success : function(data) {
			document.getElementById('request-container-'+y).remove()
			if (dummy.length == 0) {
				document.getElementById('requests-container').innerHTML = "<h1 style='text-align:center;'> No more requests </h1>"
			}
		}
	})
}