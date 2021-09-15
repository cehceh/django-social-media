function requestAccepted(pk) {
	$.ajaxSetup({
        headers: {
           	"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });
	$.ajax({
		url: 'accept/friend-request/number-'+pk,
		method: 'PUT',

		success: function() {

			$("#request-"+pk).remove();

		}

		
		}
	)

}

function requestDenied(pk) {
	$.ajaxSetup({
        headers: {
           	"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });

	$.ajax({
		url: 'deny/friend-request/number-'+pk,
		method: 'DELETE',

		success: function() {

			$("#request-"+pk).remove();

		}

		
		}
	)

}