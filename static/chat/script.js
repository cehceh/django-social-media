var chat = document.getElementById('chat-messages');
var form = document.getElementById('message-form');
function scrollToBottom() {
    let objDiv = document.getElementById("chat-messages");
    objDiv.scrollTop = objDiv.scrollHeight;
}


function ChatSocket(x, z, y) {
    const chatSocket = new WebSocket(
       'ws://'
        + window.location.host
        + '/ws/'
        + x + '/' + y + '/'
    );




    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.message) {
            document.getElementById('chat-messages').innerHTML += '<hr>' + data.message + '<br>'
            scrollToBottom();
        } else if (data.delete) {
            document.getElementById('message-'+ data.delete).remove()
        } else if (data.typing) {
            if (data.typing.z !== z) {
                if (data.typing.status == 'stop') {
                    document.getElementById('typing-status').innerHTML = ""
            }   else {
                    document.getElementById('typing-status').innerHTML = "Typing"
            }
            } 
        }
        
    };

    chatSocket.onclose = function(e) {
    };

    document.getElementById('id_content').addEventListener("input", function(){
        chatSocket.send(JSON.stringify({
            'typing': {"z":z, "status": "typing"},

        }));
    });

    document.getElementById('id_content').addEventListener("change", function(){
        chatSocket.send(JSON.stringify({
            'typing': {"z":z, "status": "stop"},
        }));
    });

        
    

}
 


    btn = document.getElementById("recorder");
    btn.addEventListener('click', function(){
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
                    btn.innerHTML = 'record';


                    document.getElementById('id_record').files = container.files;
                    document.getElementById('id_content').value = ''
                    document.getElementById('message-form').submit();
                    form.reset(); 
                }
                                        
                
                stop = document.getElementsByClassName('active')[0];
                stop.addEventListener('click', function(){
                    recorder.stop();
                    
                    
                })
                

                })


        }


                
            
    })



function sendMessage(form, pk) {
    let myForm = document.getElementById('sendMessageForm')
    let formData = new FormData(myForm)
    formData.append('pk', pk)
    $.ajaxSetup({
        headers: {
           "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                   }
            });
    $.ajax({
        url: "/chat/send-messages/",
        data: formData,
        method: 'POST',
        processData: false,
        contentType: false,
        success: function (data) {
            if (data.done == false) {
                alert("one field is at least required ")
            } else {
                form.reset()
            }         

       },
    })
        
}

function deleteMessage(argument) {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                }
        });
    $.ajax({
        method: 'POST',
        url: "/delete/message/",
        dataType: 'json',
        data : {'deleted': argument},
        success: function (data) {},
            })
        }

function DeleteMessageTrigger(pk) {
    var modal = document.createElement("div");
    modal.className = 'modal'

    var btn = document.getElementById("DeleteBtn-"+pk);

    var content = document.createElement("div");
    content.className = 'modal-content'
    modal.style.display = "block";

    content.innerHTML = ''
    var DeleteButton = document.createElement('button');
    DeleteButton.setAttribute('onclick', 'deleteMessage('+ pk +')');
    DeleteButton.innerHTML = 'Are you sure you want to delete this post?';
    DeleteButton.className = 'alert';
    content.appendChild(DeleteButton);
    modal.appendChild(content)
    document.getElementsByTagName('body')[0].appendChild(modal)

    modal.onclick = function() {
      modal.remove()
    }
}