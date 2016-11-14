const DIALOG_SYS_API = '/process_ajax';   //TO-DO: use ACTUAL dialog system API
var TOGGLE_SPEECH_SYNTHESIS = false;

/* Initial chat instructions */
setTimeout(function(){
   add_chat_entry(
      'Welcome to the Preliminator',
      {'source':'system'}
   );

   setTimeout(function(){
      add_chat_entry(
         'You may interact with the system by typing your responses,' +
         'or by clicking the microphone icon and speaking',
         {'source':'system'}
      );

      setTimeout(function(){
         add_chat_entry(
            'You can toggle speech synthesis on or off through the ' +
            '<i>options</i> dropdown above.',
            {'source':'system'}
         );

         setTimeout(function(){
            add_chat_entry(
               'To begin, send a response saying "ready"',
               {'source':'system'}
            );
         },3500);

      },3500);

   },1500);

},250);





/* When the submit button is clicked, handle_submit() */
var submit_btn = document.getElementById('submit_btn');
submit_btn.addEventListener('click',handle_submit);

/* When the enter key is pressed when typing into input, handle_submit() */
var input_box = document.getElementById('user_input_box');
input_box.addEventListener('keyup',function(event){
   event.preventDefault();
   if (event.keyCode == 13) handle_submit();
});

/* Open connection for speach API when mic button hit */
var mic_btn = document.getElementById('mic_btn');
mic_btn.addEventListener('click',function(){
   var recognition = new webkitSpeechRecognition();
   recognition.onresult = function(event) {
      document.getElementById('user_input_box').value = event.results[0][0].transcript;
      handle_submit();
      document.getElementById('user_input_box').placeholder = "Type your response, or click the microphone to speak";
   }
   recognition.start();
   document.getElementById('user_input_box').placeholder = "Listening...";
});

var toggle_sound = document.getElementById('toggle_sound');
toggle_sound.addEventListener('click',function(){
   TOGGLE_SPEECH_SYNTHESIS = !TOGGLE_SPEECH_SYNTHESIS;
   document.getElementById('toggle_sound_glyphicon').className = (TOGGLE_SPEECH_SYNTHESIS)? "glyphicon glyphicon-check" : "glyphicon glyphicon-unchecked";
   document.getElementById('audio_glyph').className = (TOGGLE_SPEECH_SYNTHESIS)? "glyphicon glyphicon-volume-up" : "glyphicon glyphicon-volume-off";

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
      if(TOGGLE_SPEECH_SYNTHESIS){
         var msg = new SpeechSynthesisUtterance(this.responseText);
         window.speechSynthesis.speak(msg);
      }
   }

   var xhr = new XMLHttpRequest();
   var fd = new FormData();
   fd.append('inputText',inputText);
   xhr.addEventListener("load", reqListener);
   xhr.open('POST',DIALOG_SYS_API);
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
