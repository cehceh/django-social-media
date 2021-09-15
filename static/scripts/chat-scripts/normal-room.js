var chat = document.getElementById('chat-messages');
var form = document.getElementById('message-form');

function scrollToBottom() {
    let objDiv = document.getElementById("chat-messages");
    objDiv.scrollTop = objDiv.scrollHeight;
}


function ChatSocket(x, y, z) {
    const chatSocket = new WebSocket(
       'ws://'
        + window.location.host
        + '/ws/'
        + x
    );





    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data)
    scrollToBottom();
    };

    chatSocket.onclose = function(e) {
    };

    document.getElementById('id_content').addEventListener("input", function(){
        chatSocket.send(JSON.stringify({
            'typing': z,

        }));
    });

    document.getElementById('id_content').addEventListener("change", function(){
        chatSocket.send(JSON.stringify({
            'typing': "stop",
        }));
    });

        
    

}
 

function eventListener() {

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


    }   

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