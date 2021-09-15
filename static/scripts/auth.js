function loginFun(btn) {
    console.log("submit")
    var form = btn.form;
    var url = "user"
    var email = document.getElementById('log_email').value;
    var password = document.getElementById('log_password').value;


    if (email.length && password.length !== 0) {
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        });

        $.ajax({
            url: url,
            method: 'POST',
            data: 
            {
                'email': email,
                'password': password
            }
            ,
            success: function (message) {
                if (message.auth == true) {
                    location.reload()
                }   
                else {
                    document.getElementsByClassName('alert')[0].style.display = 'block';
            }
        }

        })

    } else {
        document.getElementsByClassName('alert')[0].innerHTML = 'Email and password are required';
        document.getElementsByClassName('alert')[0].style.display = 'block';
    }


}


function LoginModal(div, pk, email, fullname) {
    var span = document.getElementById("close");
    var modal = document.getElementById("login-modal");
    var ImgSrc = document.getElementById("account-image-" + pk);
    var ModalImg = document.getElementById("modal-image");
    var H1 = document.getElementById("modal-h1");
    H1.innerHTML = fullname;
    ModalImg.src = ImgSrc.src;
    post_text_input = document.getElementById("modal-password");
    modal.style.display = "block";
    post_text_input.focus();

    document.getElementById("modal-email").value = email;

    span.onclick = function() {
        modal.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
          }
        }
    }



// When the user clicks on <span> (x), close the modal

// When the user clicks anywhere outside of the modal, close it


