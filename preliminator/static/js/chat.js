const DIALOG_SYS_API = '/process_ajax';   //TO-DO: use ACTUAL dialog system API
var SYNTHESIZE_RESPONSES = true;
var PAUSE_RECOGNITION = false;

window.onload = function(){
   do_initial_messages();       /* Handle initial chat messages */
   setup_speech_recognition();  /* Enable speech recognition */
   setup_synth_toggle();        /* Set up the toggle-able speech synthesis */
   add_submit_listeners();      /* Add listeners for input submission box  */
};

/* Initial chat instructions */
function do_initial_messages(){
   setTimeout(function(){
      add_chat_entry(
         "Welcome to the Preliminator, please click 'enter' or speak in to the mic to begin.",
         {'source':'system'}
      );
   },250);
}

/* Sets up continuous speech recognition. */
function setup_speech_recognition(){
   var microphone = new webkitSpeechRecognition();
   microphone.lang = 'en-US';
   microphone.continuous = true;
   microphone.lang = 'en-US';
   microphone.interimResults = false;
   microphone.maxAlternatives = 1;

   microphone.onend = function(){
      /* Restart the listener on stop, unless it's being suppressed right now */
      if(!PAUSE_RECOGNITION)
         microphone.start();
   };

   microphone.onresult = function(event){
      var results = event.results[event.results.length -1][0].transcript;
      var confidence = event.results[event.results.length -1][0].confidence;

      console.log(event.results);
      console.log('Results:\t' + results);
      console.log('Confidence:\t' + confidence);

      handle_submit(results);
   }

   microphone.start();
}

/* Sets up the toggle-able speech synthesis icon and behavior */
function setup_synth_toggle(){
   var toggle_sound = document.getElementById('toggle_synth');
   toggle_sound.addEventListener('click',function(){
      SYNTHESIZE_RESPONSES = !SYNTHESIZE_RESPONSES;   /* Flip the boolean */
      if(SYNTHESIZE_RESPONSES){
         console.log('Synth on');
         document.getElementById('toggle_synth').className = "clickable glyphicon glyphicon-volume-up";
      } else {
         console.log('Synth off');

         document.getElementById('toggle_synth').className = "clickable glyphicon glyphicon-volume-off";
         window.speechSynthesis.cancel();
      }
   });
}

/* Add listeners to check for "submit" through button click OR pressing ENTER */
function add_submit_listeners(){
   /* Add a listener so that when the submit button is clicked, handle_submit() */
   var submit_btn = document.getElementById('submit_btn');
   submit_btn.addEventListener('click',function(){
      var inputText = document.getElementById('user_input_box').value;
      handle_submit(inputText);
   });

   /* Alternative to pressing submit button: Press enter */
   var input_box = document.getElementById('user_input_box');
   input_box.addEventListener('keyup',function(event){
      event.preventDefault();
      if (event.keyCode == 13) {
         var inputText = document.getElementById('user_input_box').value;
         handle_submit(inputText);
      }
   });
}

/* Define what happens when the user submits their input */
function handle_submit(inputText){
   add_chat_entry(inputText, {'source':'user'});
   focus_on_latest_msg();

   /* Send the inputText, and set up handle_response as the callback handler */
   send_input_to_dialog(inputText, handle_response);
}

/* Sends user inputs to the dialog system through AJAX. Also takes a callback
   function to handle what to do with the response text.  */
function send_input_to_dialog(inputText, response_handling_callback){
   function reqListener () {
      response_handling_callback(this.responseText);
   }

   var xhr = new XMLHttpRequest();
   var fd = new FormData();
   fd.append('inputText',inputText);
   xhr.addEventListener("load", reqListener);
   xhr.open('POST',DIALOG_SYS_API);
   xhr.send(fd);
}

/* Define what happens when a response is received */
function handle_response(response){
   add_chat_entry(response, {'source':'system'});
   focus_on_latest_msg();
   if(SYNTHESIZE_RESPONSES){
      say(response);
   }
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
   nametag.innerHTML = (params.source === "user")? "You" : "Preliminator";
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

/* Speaks the given message, making sure to pause speech recognition while it does so. */
function say(message){
   PAUSE_RECOGNITION = true;  //Pauses speech recognition
   console.log('Listening paused');

   var utterance = new SpeechSynthesisUtterance(message);   //Creates an utterance to speak
   window.speechSynthesis.speak(utterance);                 //Begins speaking said utterance

   /* When done speaking, restore speech recognition. */
   utterance.addEventListener('end',function(){
      PAUSE_RECOGNITION = false;
      console.log('Listening restored');
   });
}
