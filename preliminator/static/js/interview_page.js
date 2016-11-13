const DIALOG_SYS_API = '/process_ajax';   //TO-DO: use ACTUAL dialog system API

/* When the button is clicked, handle_submit() */
var submit_btn = document.getElementById('submit_btn');
submit_btn.addEventListener('click',handle_submit);

/* When the enter key is pressed when typing into inpu, handle_submit() */
var input_box = document.getElementById('user_input_box');
input_box.addEventListener('keyup',function(event){
   event.preventDefault();
   if (event.keyCode == 13) handle_submit();
});

/* Define what happens when the user submits their input */
function handle_submit(){
   var inputText = document.getElementById('user_input_box').value;
   add_chat_entry(inputText, {'source':'user'});
   focus_on_latest_msg();
   send_input_to_dialog(inputText, handle_response);
}

/* Define what happens when a response is received */
function handle_response(response){
   add_chat_entry(response, {'source':'system'});
   focus_on_latest_msg();
}

function send_input_to_dialog(inputText, callback){
   function reqListener () {
      callback(this.responseText);
   }

   var xhr = new XMLHttpRequest();
   var fd = new FormData();
   fd.append('inputText',inputText);
   xhr.addEventListener("load", reqListener);
   xhr.open('GET',DIALOG_SYS_API);
   xhr.send(fd);

}

/* Scroll down to make latest chatEntry visible */
function focus_on_latest_msg(){
   var boxes = document.getElementsByClassName('chatEntry');
   var last_box = boxes[boxes.length -1];
   last_box.scrollIntoView(true);
}

/* Adds a chatEntry element containing some inputString*/
function add_chat_entry(inputString, params){

   var frag = document.createDocumentFragment();

   var divNeeded = document.getElementById("add-messages");

   var chatEntry = document.createElement('div');
   chatEntry.className = "chatEntry row";

   var chatBox = document.createElement('div');
   chatBox.className = (params.source === "system")? "col-xs-9" : "col-xs-9 col-xs-offset-1";
   var chat_text_div = document.createElement('div');
   chat_text_div.className = "chat-bubble";
   chat_text_div.innerHTML = inputString;
   chatBox.appendChild(chat_text_div);

   var meta_chat_div = document.createElement('div');
   meta_chat_div.className = (params.source === "user")? "col-xs-1" : "col-xs-1 col-xs-offset-1";
   var pic_name_div = document.createElement('div');
   if(params.source === "user")
      pic_name_div.className = "user-pic-n-name";
   var pic = document.createElement('img');
   var picSource = (params.source === "user")? "../static/media/user.png" : "../static/media/user.gif";
   pic.setAttribute('src', picSource);
   pic.className = (params.source === "system")? "img-rounded-sq interviewer-pic":"img-rounded-sq interviewee-pic";
   pic_name_div.appendChild(pic);
   var nametag = document.createElement('h5');
   nametag.innerHTML = (params.source === "user")? "You" : "Interviewer";
   pic_name_div.appendChild(nametag);
   meta_chat_div.appendChild(pic_name_div);

   if(params.source === "user"){
      chatEntry.appendChild(chatBox);
      chatEntry.appendChild(meta_chat_div);
   } else {
      chatEntry.appendChild(meta_chat_div);
      chatEntry.appendChild(chatBox);
   }

   var hr = document.createElement('hr');

   frag.appendChild(hr);

   frag.appendChild(chatEntry);

   divNeeded.appendChild(frag);

   // reset the message box
   var inputTag = document.getElementById('user_input_box').value = "";
}