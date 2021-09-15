function errorModal(message) {

	var modal = document.createElement("div");
	modal.className = 'modal'

	var span = document.createElement("span");
	span.className = 'close'
	
	var content = document.createElement("div");

	modal.style.display = "block";

	content.innerHTML = ''
	content.appendChild(span);
	modal.appendChild(content)
	document.getElementsByTagName('body')[0].appendChild(modal)

	content.innerHTML += '<div> <p> ' + message + '</p> </div>'

	modal.onclick = function() {
		modal.style.display = 'none'
	}
}


function DisplayFullImg(img) {
	var modal = document.createElement('div');
	modal.className = 'modal';
	var span = document.createElement("span");
	span.className = 'modal-close';
	span.innerHTML = '&times;';
	var content = document.createElement("div");
	content.className = 'modal-content'
	modal.appendChild(content)
	content.appendChild(span)
	modal.style.display = "block";
	src = img.src;
	image = document.createElement("img")
	image.src = src;
	content.appendChild(image);

	span.onclick = function() {
	  modal.style.display = "none";
	}

	window.onclick = function(event) {
	  if (event.target == modal) {
		modal.style.display = "none";
	  }
	}

}

function ShowReveiwPost() {
	document.getElementById('ModalReveiwPost').style.display = 'block';
}

function ReveiwPost(input) {

	var modal = document.createElement("div");
	modal.id = "ModalReveiwPost"
	modal.className = 'modal'


	var content = document.createElement("div");
	modal.appendChild(content)
	content.className = 'modal-content'
	document.getElementsByTagName('body')[0].appendChild(modal)
	modal.style.display = "block";

	content.innerHTML = ''

	modal.onclick = function() {
	  modal.style.display = "none";
	}

	var reveiwPostButton = document.createElement('button')
	reveiwPostButton.innerHTML = "reveiw"
	reveiwPostButton.id = 'reveiwPostButton'
	reveiwPostButton.setAttribute('onclick' , "ShowReveiwPost()")
	document.getElementById('uploading-form').appendChild(reveiwPostButton)
	
	 var i;
	if (input.files.length == 1) {

		if (input.files[0].name.split('.').pop() == 'mp4') {
			if (document.getElementById('video_0')) {
				document.getElementById('video_0').remove();
			}
			
			content.innerHTML = "";
			content.innerHTML += '<video src="" controls width="100%" height="200px" name='+'video_'+[0]+' id='
			+ 'video_' +[0]+'> </video> <br>';

			document.getElementById('video_'+[0]).src = URL.createObjectURL(input.files[0]);
			input.value == input.files[0]
			
		
		} else {
			if ( null != document.getElementById('img_0') ) {
				document.getElementById('img_0').remove();
			}
			
			content.innerHTML = '<br> <img src=' + input.files[0] +' + width="400px" height="400px" name='+'img_'+[0]+' id='+'img_'+[0]+'> </img>' + '<br>';
			document.getElementById('img_'+[0]).src = URL.createObjectURL(input.files[0]);
			input.value == input.files[0]
		}

	} else {

		content.innerHTML = "";

		for (i = 0; i < input.files.length; i++) {

			if (input.files[i].name.split('.').pop() == 'mp4') {

				content.innerHTML += '<video src="" width="100%" height="200px" name='+'video_'+[i]+' id='
				+ 'video_' +[i]+'>' + '<br>' + '<input type="text" name=' + 'video_caption_' + [i] +  '> </video> <br>';
				document.getElementById('video_'+[i]).src = URL.createObjectURL(input.files[i]);
			
			} else {
				br = document.createElement('br')
				img = document.createElement('img')
				img.style.width = "400px"
				img.style.headers = "400px"
				img.name = "img_" + [i]
				img.id = img.name
				content.appendChild(br)
				content.appendChild(img)
				content.appendChild(br)
				img.src = URL.createObjectURL(input.files[i]);
			}

			}
	}
	

		};



function postImagesDisplay(pk, url, index, caption) {
	console.log(pk)
	var oldIndicators = document.getElementsByClassName('post-'+pk+'-indicators');
	for (var i = oldIndicators.length - 1; i >= 0; i--) {
		oldIndicators[i].style.backgroundColor = "grey";
	}

	var newIndicator = document.getElementsByClassName('post-'+pk+'-indicators')[index-1];
	newIndicator.style.backgroundColor = 'white';

	var container = document.getElementById('post-' + pk + '-media-display');
	var img = document.createElement('img');
	img.src = url;
	img.setAttribute('onclick', "DisplayFullImg(this);")
	container.innerHTML = '';
	container.appendChild(img);
	if (caption == "None") {
		caption = ""
	} 


	document.getElementById('post-'+pk+'-files-caption').innerHTML = "<br>" + caption + "<br>"
		
}

function postVideosDisplay(pk, url, index, caption) {

	var oldIndicators = document.getElementsByClassName('post-'+pk+'-indicators');


	for(var i = 0; i < oldIndicators.length; i++){
		oldIndicators[i].style.backgroundColor = "grey";
	}

	var newIndicator = document.getElementsByClassName('post-'+pk+'-indicators')[index-1];
	newIndicator.style.backgroundColor = 'white';

	var container = document.getElementById('post-' + pk + '-media-display');
	var video = document.createElement('video');
	video.setAttribute('controls', "")
	video.src = url;	

	container.innerHTML = '';
	container.appendChild(video);

	if (caption == "None") {
		caption = ""
	} 
	
	document.getElementById('post-'+pk+'-files-caption').innerHTML = "<br>" + caption + "<br>"
}

function postRecordsDisplay(pk, url, index, caption) {

	var oldIndicators = document.getElementsByClassName('post-'+pk+'-indicators');

	for(var i = 0; i < oldIndicators.length; i++){
		oldIndicators[i].style.backgroundColor = "grey";
	}


	var newIndicator = document.getElementsByClassName('post-'+pk+'-indicators')[index-1];
	newIndicator.style.backgroundColor = 'white';

	var container = document.getElementById('post-' + pk + '-media-display');
	var audio = document.createElement('audio');
	var src = document.createElement('source');
	src.src = url;
	audio.appendChild(src)
	audio.src = url;	
	container.innerHTML = '';
	container.appendChild(audio);

	if (caption == "None") {
		caption = ""
	} 
	
	document.getElementById('post-'+pk+'-files-caption').innerHTML = "<br>" + caption + "<br>"
}


function DeletePost(pk) {
	var modal = document.getElementById("myModal");
	var span = document.getElementsByClassName("close")[0];
				
	$.ajaxSetup({
		headers: {
			"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
		}
	});

	$.ajax({
		url: 'delete/post/number-'+pk,
		method: 'DELETE',

		success: function(message) {
			if (message.done == true) {
				document.getElementById('post-'+pk).remove();
				modal.style.display = 'none';
			} else {
				modal.innerHTML = span;
				modal.innerHTML += '<h1 style="color:white;">Something went wrong, please try again </h1>'
			}

		}

		
		}
	)
}




function sharedpostImagesDisplay(pk, url, index, caption) {
	console.log(pk)
	var oldIndicators = document.getElementsByClassName('shared-post-'+pk+'-indicators');
	for (var i = oldIndicators.length - 1; i >= 0; i--) {
		oldIndicators[i].style.backgroundColor = "grey";
	}

	var newIndicator = document.getElementsByClassName('shared-post-'+pk+'-indicators')[index-1];
	newIndicator.style.backgroundColor = 'white';

	var container = document.getElementById('shared-post-' + pk + '-media-display');
	var img = document.createElement('img');
	img.src = url;
	img.setAttribute('onclick', "DisplayFullImg(this);")
	container.innerHTML = '';
	container.appendChild(img);
	if (caption == "None") {
		caption = ""
	} 


	document.getElementById('shared-post-'+pk+'-files-caption').innerHTML = "<br>" + caption + "<br>"
		
}

function sharedpostVideosDisplay(pk, url, index, caption) {

	var oldIndicators = document.getElementsByClassName('shared-post-'+pk+'-indicators');


	for(var i = 0; i < oldIndicators.length; i++){
		oldIndicators[i].style.backgroundColor = "grey";
	}

	var newIndicator = document.getElementsByClassName('shared-post-'+pk+'-indicators')[index-1];
	newIndicator.style.backgroundColor = 'white';

	var container = document.getElementById('shared-post-' + pk + '-media-display');
	var video = document.createElement('video');
	video.setAttribute('controls', "")
	video.src = url;	

	container.innerHTML = '';
	container.appendChild(video);

	if (caption == "None") {
		caption = ""
	} 
	
	document.getElementById('shared-post-'+pk+'-files-caption').innerHTML = "<br>" + caption + "<br>"
}

function sharedpostRecordsDisplay(pk, url, index, caption) {

	var oldIndicators = document.getElementsByClassName('shared-post-'+pk+'-indicators');

	for(var i = 0; i < oldIndicators.length; i++){
		oldIndicators[i].style.backgroundColor = "grey";
	}


	var newIndicator = document.getElementsByClassName('shared-post-'+pk+'-indicators')[index-1];
	newIndicator.style.backgroundColor = 'white';

	var container = document.getElementById('shared-post-' + pk + '-media-display');
	var audio = document.createElement('audio');
	var src = document.createElement('source');
	src.src = url;
	audio.appendChild(src)
	audio.src = url;	
	container.innerHTML = '';
	container.appendChild(audio);

	if (caption == "None") {
		caption = ""
	} 
	
	document.getElementById('shared-post-'+pk+'-files-caption').innerHTML = "<br>" + caption + "<br>"
}



function DeletePostTrigger(pk) {
	var modal = document.getElementById("myModal");

	var btn = document.getElementById("DeleteBtn-"+pk);

	var span = document.getElementById("modal-close");

	var content = document.getElementById("modal-content");
	modal.style.display = "block";

	content.innerHTML = ''
	var DeleteButton = document.createElement('button');
	DeleteButton.setAttribute('onclick', 'DeletePost('+ pk +')');
	DeleteButton.innerHTML = 'Are you sure you want to delete this post?';
	DeleteButton.className = 'alert';
	content.appendChild(DeleteButton);
	content.appendChild(span);

	span.onclick = function() {
	  modal.style.display = "none";
	}

	window.onclick = function(event) {
	  if (event.target == modal) {
		modal.style.display = "none";
	  }
	}
}
function ShowCommentsContainer(pk) {
	var container = document.getElementById("post-" + pk + "-comments-container");
	container.style.display = 'block';

}
function ShowComments(pk, btn) {
	var container = document.getElementById("post-" + pk + "-comments-container");
	var div = document.getElementById("post-"+pk+"-comments-div")
	var counter = btn.dataset.count
	$.ajaxSetup({
		headers: {
			"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
		}
	});

	$.ajax({
		url: 'get/10-comments/on/post-number/' + pk + '/' + counter,
		success: function(data) {
			console.log(data);
			if (data.message) {
				console.log(data.message)
				errorModal(data.message)

			} else {
				$(btn).attr('data-count', counter + data.length)
				btn.setAttribute('onclick', 'ShowCommentsContainer("' + pk + '")');
				for (var i = data.length - 1; i >= 0; i--) {
					div.innerHTML += data[i]
				} container.dataset.count = parseInt(counter) + parseInt(data.length)

			}

		}

		
		}
	)

	if (container.style.display == 'block') {
		container.style.display = 'none';
	} else {
		container.style.display = 'block'
	}

	document.getElementById('post-' + pk + '-comments-close-span').onclick = function(){
		container.style.display = 'none'
	}
}

function SubmitComment(form, pk) {
	commentData = new FormData(form)
	$.ajax({
		headers: {
			"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
		},
		cache: false,
		contentType: false,
		processData: false,
		url:'/comment/'+pk,
		method:'POST',
		data:commentData,
		success: function (data){
			if (data.comment) {
				var div = document.getElementById("post-"+pk+"-comments-div")
				div.innerHTML += data.comment
			}
		}
	})
}

function topActions(pk) {
	var container = document.getElementById("post-" + pk + "-top-actions-container");
	var btn =  document.getElementById("post-" + pk + "-top-trigger");
	var containers = document.getElementsByClassName("post-top-actions-container");

	

	if (container.style.display == 'none') {

		for (var i = containers.length - 1; i >= 0; i--) {
			containers[i].style.display = 'none';
		}

		container.style.display = 'block';

	} else {

		container.style.display = 'none';
	}

	window.onclick = function(event) {
	  if (event.target !== container &&  event.target !== btn && container.style.display == 'block' ) {
		container.style.display = "none";
	  } 
	}

}


function SharedtopActions(first, second) {
	var container = document.getElementById("shared-" + first + "-post-" + second + "-top-actions-container");
	var btn =  document.getElementById("shared-" + first + "-post-" + second + "-top-trigger");
	var containers = document.getElementsByClassName("post-top-actions-container");

	

	if (container.style.display == 'none') {

		for (var i = containers.length - 1; i >= 0; i--) {
			containers[i].style.display = 'none';
		}

		container.style.display = 'block';

	} else {

		container.style.display = 'none';
	}

	window.onclick = function(event) {
	  if (event.target !== container &&  event.target !== btn && container.style.display == 'block' ) {
		container.style.display = "none";
	  } 
	}

}

function showReactsBox(btn, argument) {

	var isOnBtn = true;

	btn.addEventListener("mouseout", function(  ) {
		isOnBtn = false;
		isOnDiv = false;
		setTimeout(function() {

			if (isOnBtn == false && isOnDiv == false) {

				container.style.display = 'none';
			}

		

		}, 500);

	});

	var container = document.getElementById('post-' + argument + '-react-container');

	setTimeout(function() {

		if (isOnBtn == true) {

			container.style.display = 'flex';
		}

		

	}, 500);

	container.addEventListener("mouseover", function(  ) {isOnDiv=true});

	container.addEventListener("mouseout", function(  ) {
		isOnDiv = false;

		setTimeout(function() {

			if (isOnBtn == false && isOnDiv == false) {

				container.style.display = 'none';
			}

		

		}, 500);
		
	});


}




function PostReact(_type, pk) {

	$.ajaxSetup({
		headers: {
			"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
		}
	});

	$.ajax({
		url: '/' + _type + '/post-number/'+pk,
		success: function(message) {
			if (! message.blocked) {

				document.getElementById('post-' + pk + '-middle').innerHTML = message
				
			} else if (message.blocked == true) {
				
				document.getElementById('post-'+pk).remove()
			}

		}

		
		}
	)
}

function RemovePostReact(pk) {
		$.ajaxSetup({
		headers: {
			"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
		}
	});

	$.ajax({
		url: '/remove-react/on/post-number/'+pk,
		success: function(message) {
			if (! message.fail) {

				document.getElementById('post-' + pk + '-middle').innerHTML = message
				
			} else {
				var modal = document.getElementById("myModal");
				modal.style.display = "block";
				var span = document.getElementById("modal-close");
				var content = document.getElementById("modal-content");
				content.innerHTML += span;
				modal.appendChild(content);
				content.innerHTML = message.data;

				setTimeout(function() {
					modal.style.display = 'none';
				}, 1000);

			}

		}

		
		}
	)
}


function postUpload(argument, pk, _type) {

	if (document.getElementById("post-content-input").value.length !== 0 || document.getElementById("post-files-input").value.length !== 0 ) {

		if (_type == 1) {

			post_url = 'post/on/group/'+pk

		} else if (_type == 2) {

			post_url = 'post'

		} else {

			post_url = 'post/on/page/'+ pk
		}

		$form = $(argument)
		var formData = new FormData(argument);

		$.ajax({

			url:  post_url,
			type: 'POST',
			data: formData,
			xhr: function() {
			    var xhr = new window.XMLHttpRequest();

			        UploadDiv = document.getElementById('uploading-form');

			        progressDiv = document.createElement('div')
			        progressDiv.id = 'progress-div-id';

			        progressDiv.className = 'progress';
			        UploadDiv.appendChild(progressDiv);



			        progressBar = document.createElement('div')
			        progressBar.className = 'progress-bar';
			        progressDiv.appendChild(progressBar);

			        span = document.createElement('span');
			        span.className = 'sr-only';
			        progressBar.appendChild(span);

			        progressBar.setAttribute("role", "progressbar");
			        progressBar.setAttribute("aria-valuemin", "0");
			        progressBar.setAttribute("aria-valuemax", "100");
			        UploadDiv.appendChild(progressDiv);

			    xhr.upload.addEventListener("progress", function(evt) {
			      if (evt.lengthComputable) {
			        var percentComplete = evt.loaded / evt.total;
			        percentComplete = parseInt(percentComplete * 100);

			        progressBar.style.width = percentComplete + "%";

			        progressBar.setAttribute("aria-valuenow", percentComplete);



			        
			        span.innerHTML = percentComplete + "% completed."

			        if (percentComplete === 100) {

			        	setTimeout(function(){ 

			        		document.getElementById('progress-div-id').remove();
			        		if (document.getElementById('post-content-input').type == 'file') {
			        			document.getElementById('post-content-input').type = 'text';
								document.getElementById('post-content-input').style.display = 'block';
			        		}
			        		

			        	 }, 2000);

			        }

			      }
			    }, false);

			    return xhr;
			  },
			success: function (response) {
				if(response.success){

					location.reload()

				}
				else{
					alert(response.messages)
				}
			},
			cache: false,
			contentType: false,
			processData: false
		});


		


		
		


	} else {

		alert("at least one field is required");
	}
	
}


function shareModal(pk) {



	var modal = document.createElement("div");
	modal.className = 'modal'
	var span = document.getElementById("span");
	span.className = 'close'

	var content = document.createElement("div");
	content.className = 'modal-content'

	modal.style.display = "block";

	content.innerHTML = ''
	content.appendChild(span);
	
	var share_btn = document.createElement("button");
	var caption = document.createElement("input");
	caption.type = "text";
	caption.id = "sharing-post-"+pk
	content.appendChild(caption)
	caption.name = "caption"
	share_btn.setAttribute('onclick', 'PostShare(' + pk + ')')
	share_btn.innerHTML = 'Share post'
	share_btn.className = 'action-btn'
	content.appendChild(share_btn);
	modal.style.display = "block";
	modal.appendChild(content)
	document.getElementsByTagName('body')[0].appendChild(modal)
			


	span.onclick = function() {
	  modal.remove()
	}

	window.onclick = function(event) {
	  if (event.target == modal) {
		modal.remove()
	  }
	}

}


function PostShare(pk) {

	$.ajaxSetup({
		headers: {
			"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
		}
	});

	$.ajax({
		method: 'POST',
		url: 'share/post/'+pk,
		data: {
			'caption': document.getElementById('sharing-post-'+pk).value,
		},
		success: function(message) {
			if (message.counts) {
					document.getElementById("myModal").style.display = 'none';
					document.getElementById('post-share-icon-' + pk).className = 'fas fa-share';
					document.getElementById('post-' + pk + '-react-button').innerHTML = message.counts;
			} else {
				errorModal(message.data)
			}

		}

		
		}
	)

}

function openNotify(pk) {
	$.ajaxSetup({
		headers: {
			"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
		}
	});

	$.ajax({
		url: 'activate/post/'+pk+ '/notifies',
		success: function(message) {
			if (message.error) {
					errorModal(message.error);
			} 

		 	document.getElementById("post-" + pk + "-top-actions-container").style.display ='none'

		}

		
		}
	)
}

function SavePost(pk) {
	$.ajaxSetup({
		headers: {
			"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
		}
	});

	$.ajax({
		method: 'POST',
		url: '/save/post/',
		data: {'pk':pk},
		success: function(message) {
			if (message.error) {
					errorModal(message.error);
			} 
			
		 	document.getElementById("post-" + pk + "-top-actions-container").style.display ='none'

		}

		
		}
	)
}



function Record() {

    btn = document.getElementById("recorder");
        if (btn.className == 'not-active') {
            btn.className = 'active';
            btn.innerHTML = 'recording';
            var device = navigator.mediaDevices.getUserMedia({audio: true});
            var items = [];
            device.then(function(stream) {
                var recorder = new window.MediaRecorder(stream);
                recorder.start();
                recorder.ondataavailable = function(e){
                    items.push(e.data);

                }

                recorder.onstop = function(){
                    var blob = new Blob(items, {type: 'audio/ogg; codecs=opus'});
                    const audio_url = window.URL.createObjectURL(blob);

                    let record = new File([blob], "record-name.ogg", { type: 'audio/ogg; codecs=opus', lastModified:new Date().getTime()});
                    let container = new DataTransfer();
                    container.items.add(record);
                    btn.className = 'not-active';
                    btn.innerHTML = 'recording';
                    document.getElementById('post-content-input').type = 'file';
                    document.getElementById('post-content-input').files = container.files;
                	document.getElementById('post-content-input').style.display = 'none';
                }

                btn.addEventListener('click', function(){
                    recorder.stop();
                    btn.innerHTML = 'Recorder'
                    btn.className = 'not-active'
                })
                })
        }

    }   
function ShareRecord(pk) {

    btn = document.getElementById("share-recorder-"+pk);
        if (btn.className == 'not-active') {
            btn.className = 'active';
            btn.innerHTML = 'recording';
            var device = navigator.mediaDevices.getUserMedia({audio: true});
            var items = [];
            device.then(function(stream) {
                var recorder = new window.MediaRecorder(stream);
                recorder.start();
                recorder.ondataavailable = function(e){
                    items.push(e.data);

                }

                recorder.onstop = function(){
                    var blob = new Blob(items, {type: 'audio/ogg; codecs=opus'});
                    const audio_url = window.URL.createObjectURL(blob);

                    let record = new File([blob], "record-name.ogg", { type: 'audio/ogg; codecs=opus', lastModified:new Date().getTime()});
                    let container = new DataTransfer();
                    container.items.add(record);
                    btn.className = 'not-active';
                    btn.innerHTML = 'recording';
                    document.getElementById('sharing-post-'+ pk).type = 'file';
                    document.getElementById('sharing-post-'+ pk).files = container.files;
                	document.getElementById('sharing-post-'+ pk).style.display = 'none';
                }

                btn.addEventListener('click', function(){
                    recorder.stop();
                    btn.innerHTML = 'Recorder'
                    btn.className = 'not-active'
                })
                })
        }

    }   

function notifyAccepted(argument) {
	// body...
}

function notifyDenied(argument) {
	// body...
}

function searchDiv(label) {
	if (label.className == 'search-icon not-activated') {

		label.classList.remove("not-active");
		label.classList.add("active");
		document.getElementById('searchModal').style.display = 'block';

		document.getElementById('SearchModal-close').onclick = function() {
		  document.getElementById('searchModal').style.display = "none";
		}

		window.onclick = function(event) {
		  if (event.target == document.getElementById('searchModal')) {
			document.getElementById('searchModal').style.display = "none";
		  }
		}


	} else {
		label.classList.remove("active");
		label.classList.add("not-active");
		document.getElementById('searchModal').style.display = 'none';
	}
}