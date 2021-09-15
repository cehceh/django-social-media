

function socket(pk) {

	const HomeSocket = new WebSocket(
                'ws://'
                + window.location.host
                + '/ws/home/' + pk + '/'
            );
            

            HomeSocket.onmessage = function(e) {

                const data = JSON.parse(e.data);

                console.log(data)
                if (data.notify) {

                    if (document.getElementById('no-notifies')) {
                        document.getElementById('no-notifies').style.display = 'none';}
                    var container = document.getElementById('notifies-ul');
                    container.innerHTML += data.notify



                } else if (data.notify_delete) {




                    document.getElementById("notify-"+data.notify_delete).remove();


                    if (document.getElementsByClassName('notification-container').length == 0) {

                        document.getElementById('no-notifies').style.display = 'block';
                    }

                
                }  else if (data.request_pk) {


                    var container = document.getElementById('requests-ul');
                    container.innerHTML += data.request_pk
                    



                } else if (data.request_delete) {
                    console.log(data.request_delete)
                    if (document.getElementById("request-"+data.request_delete)) {
                        document.getElementById("request-"+data.request_delete).remove();
                    }
                } else if (data.message){
                    console.log(data.message)
                    if (document.getElementById('nav-message-'+ data.message.id)) {
                        document.getElementById('nav-message-'+ data.message.id).innerHTML = data.message.nav_m
                    } else { 
                        if (document.getElementById('no-Messages')) {
                            document.getElementById('no-Messages').remove()
                        }
                        document.getElementById('Messages-ul').innerHTML += data.message.nav_m
                    }
                }
            };  
            HomeSocket.onclose = function(e) {
            };
}

            