// method to dynamically add javascript into the interview page chat box
// user will be 0 for interviewer and 1 for candidate

// build fragment and then add it to the document of interest
//var myLink = document.getElementById('clickMe');

var inputString;

function pop(user){
    // create fragment to add in
    // think of it as the base fragment
    var frag = document.createDocumentFragment();

    //pulls the correct input tag
    var inputTag = document.getElementById('banana');
    
    // grabs the entered value string
    // this is what we will use to populate html with
    inputString = inputTag.value;
        
    // get the right div tag
    // this is where we want to add in the html
    var divNeeded = document.getElementById("add-messages");


    // to add in the correct values, probably a better way but eh, i dont know javascript
    // defne each inner tag as its own document element
    var chatEntry = document.createElement('div');
    chatEntry.className = "chatEntry";

    var chatBoxLeft = document.createElement('div');
    chatBoxLeft.className = "chat-box-left";
    chatBoxLeft.innerHTML = inputString;

    var chatBoxNameLeft = document.createElement('div');
    chatBoxNameLeft.className = "chat-box-name-left";

    var imgTag = document.createElement('img');
    imgTag.src = "../chat-box/assets/img/user.png";
    imgTag.alt = "bootstrap Chat box user image";
    imgTag.className = "img-circle";
    chatBoxNameLeft.appendChild(imgTag);

    var hr = document.createElement('hr');
    hr.className = "hr-class";

    chatEntry.appendChild(chatBoxLeft);
    chatEntry.appendChild(chatBoxNameLeft);
    chatEntry.appendChild(hr);

    // now that the nesting of tags is taken care of, add into html
    divNeeded.appendChild(frag);

    // reset the message box
    inputTag.value = "";

    //var innerMediatag = contents3.appendChild(mediaBodyDiv);
     

    //contents.appendChild(.createTextNode('hi'));

    //divNeeded.appendChild(frag);

    // check to make sure its still linked
    //if(user == 1){
    //    alert('hi');
    //}

    // the intro to each message added into the chat conversation
    //var introString = '<li class="media"><div class="media-body"><div class="media">';

    // the header for the next part of the html chunk is dependent on interviewer or candidate
    //var interviewer = '<a class="pull-left" href="#"><img class="media-object img-circle " src="../bootstrap-chat-example/assets/img/interviewer.png" /></a><div class="media-body" >';
    //var candidate = '<a class="pull-left" href="#"><img class="media-object img-circle " src="../bootstrap-chat-example/assets/img/cat.png" /></a><div class="media-body" >';
    
    // closing tags
    //var endingString = '</div></div></div></li>';

/*
    var htmlToAdd;
    // yay javascript just uses + signs to add things together
    if(user == 0){
        htmlToAdd = introString + interviewer + inputString + endingString;
    }
    else if (user == 1){
        htmlToAdd = introString + candidate + inputString + endingString;
    }
    else{
        alert('yo you fucked up')
    }
*/

    //contents.appendChild(document.createTextNode(htmlToAdd));

    //divNeeded.appendChild(frag);
    //divNeeded.appendChild(document.createElement('div'));
}

// TO DO
// need to grab the value of the input line above to submit that data on button
// click

/*
function populate(htmlStr, textToAdd, user) {
    var frag = document.createDocumentFragment(),
        temp = document.createElement('div');
    
    // pulling the div tag to add to
    var divNeeded = document.getElementById("add-messages");

    // automatically changes the html to add
    //temp.innerHTML = htmlStr;
    
    //while (temp.firstChild) {
    //    frag.appendChild(temp.firstChild);
    //  }
    //    return frag;
    //}

    // the intro to each message added into the chat conversation
    var introString = '<li class="media"><div class="media-body"><div class="media">';

    // the header for the next part of the html chunk is dependent on interviewer or candidate
    var interviewer = '<a class="pull-left" href="#"><img class="media-object img-circle " src="../bootstrap-chat-example/assets/img/interviewer.png" /></a><div class="media-body" >';
    var candidate = '<a class="pull-left" href="#"><img class="media-object img-circle " src="../bootstrap-chat-example/assets/img/cat.png" /></a><div class="media-body" >';
    
    // closing tags
    var endingString = '</div></div></div></li>';

    // yay javascript just uses + signs to add things together
    if(user == 0){
        var htmlToAdd = introString + interviewer + textToAdd + endingString;

    }
    else if (user == 1){
        var htmlToAdd = introString + candidate + textToAdd + endingString;
    }
    else{
        console.log('yo you fucked up')
    }

    // next step divNeeded.appendChild(fragment)

    document.getElementById("add-messages").appendChild(fragment);     
    //document.body.insertBefore(fragment, document.body.childNodes[0]);

*/

