async function send(){

let name=document.getElementById("name").value;
let email=document.getElementById("email").value;
let message=document.getElementById("message").value;

let res=await fetch("/contact",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({name,email,message})
});

document.getElementById("status").innerText="Message Sent!";
}
