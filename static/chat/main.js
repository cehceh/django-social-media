let nav = document.querySelector(".nav-bar");
let navWidth = getComputedStyle(nav).width;
let input = document.querySelector(".inputs input");
let textarea =document.getElementById("textarea");

window.onload = function(){
    // document.body.style.height = window.screen.height;
    nav.style.left = "-" + navWidth;

    if(window.screen.availWidth <= 800){
        textarea.style = "display:block;";
        textarea.style.maxWidth = "120px";
        textarea.style.minWidth = "120px";
        textarea.style.maxHeight = "30px";
        textarea.style.minHeight = "30px";
        input.style = "display:none";

    }else{
        textarea.style = "display:none;";
        input.style = "display:block";
    }
};

            /* اظهار قائمة النيف بار الجانبى */
let cloth = document.querySelector(".cloth");

cloth.addEventListener("click" , function(){
    if(nav.style.left <= ("-" + navWidth)){
        nav.style.left = "0px"
    }else{
        nav.style.left = "-" + navWidth;
    }
})

        /* اظهار قائمة التعديل والرد والحذف */

let messageOptions = document.querySelectorAll(".message-options");
let decision = document.querySelector(".decision");
let threePoints = Array.from(messageOptions);

threePoints.forEach(function(ele){
    ele.addEventListener("click" , function(){
        threePoints.forEach(function(ele){
            ele.parentElement.querySelector(".decision").classList.remove("scale-1");
        })
        this.parentElement.querySelector(".decision").classList.toggle("scale-0");
        this.parentElement.querySelector(".decision").classList.toggle("scale-1");
        /* اغلاق بوكس الرد على الرسايل */
        // document.querySelector(".replay-container").style = "transform: translate(-50% , -50%) scale(0);"

    })
})
        /* اخفاء قايمة التعديل والرد والحذف عند الضغط على اى منها */

let editReplyRemove = Array.from(document.querySelectorAll(".edit-reply-remove div"));

editReplyRemove.forEach(function(ele){
    ele.addEventListener("click" , function(){
        this.parentElement.classList.remove("scale-1")
    })
})
        /* اظهار قائمة الكاميرا والريكورد والايموجى */

let clip = document.querySelector(".clip");
let clipOptions = document.querySelector(".clip-options");

clip.addEventListener("click" , function(){

    if(clipOptions.style.maxWidth >= "100px"){
        clipOptions.style.maxWidth = "0px"
    }else{
        clipOptions.style.maxWidth = "100px"
    }
    // clipOptions.classList.toggle("widthUp");
    // clipOptions.classList.toggle("clip-options");
})

        /* اظهار الصورة والفيديو فى حجم الشاشة عند الضغط عليها */

let fullScreen = document.querySelector("#full-screen");
let scaleImg= Array.from(document.querySelectorAll("#chat-message img"));
let scaleVideo= Array.from(document.querySelectorAll("#chat-message video"));

scaleImg.forEach(function(ele){
    ele.addEventListener("click" , function(){
        fullScreen.style = "transform: scale(1)"
        fullScreen.querySelector("img").src = this.src;
    })
})
scaleVideo.forEach(function(ele){
    ele.addEventListener("click" , function(){
        fullScreen.style = "transform: scale(1)"
        fullScreen.querySelector("video").src = this.src;
    })
})

        /* تعديل حجم الصور والفيديو فى الشات */

scaleImg.forEach(function(ele){
    if(ele.getAttribute("src").length >= 2){
        ele.style = `
            width: 150px;
            height: 180px;
            border-radius: 10px;
            cursor: pointer;
        `
    }else{
        ele.style = `
            width: 0;
            height: 0px;
            overflow: hidden;
        `
    }
})
scaleVideo.forEach(function(ele){
    if(ele.getAttribute("src").length >= 2){
        ele.style = `
            width: 150px;
            height: 180px;
            border-radius: 10px;
            cursor: pointer;
            background: darkolivegreen;
        `
    }else{
        ele.style = `
            width: 0;
            height: 0px;
            overflow: hidden;
        `
    }
})

let reply = Array.from(document.querySelectorAll(".edit-reply-remove .reply"));
let replayContainer = document.querySelector(".replay-container");
let clothReplayContainer = document.querySelector(".cloth-replay-container");

    /* اظهار بوكس الرد على الرسايل */
reply.forEach(function(ele){

    ele.addEventListener("click" , function(){
        
        replayContainer.querySelector("div span").innerHTML = this.parentElement.parentElement.querySelector(".message .actually-message").innerHTML
        replayContainer.style = "transform: translate(-50% , -50%) scale(1);"
        
    })

})
        /* اغلاق بوكس الرد على الرسايل */

clothReplayContainer.addEventListener("click" , function(){
    replayContainer.style = "transform: translate(-50% , -50%) scale(0);"
})

let sendReplay = document.querySelector("#send-replay");

sendReplay.addEventListener("click" , function(){
    clothReplayContainer.click();
})
        /* حذف الرسايل */

let remove = Array.from(document.querySelectorAll(".edit-reply-remove .remove"));
remove.forEach(function(ele){
    ele.addEventListener("click" , function(){
        $.ajax({
            headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
            method: 'DELETE',
            url: '/delete/message/',
            data: {'id': ele.dataset.id},
        })
        
    })
});
