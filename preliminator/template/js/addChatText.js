// method to dynamically add javascript into the interview page chat box
// user will be 0 for interviewer and 1 for candidate

// build fragment and then add it to the document of interest
//var myLink = document.getElementById('clickMe');

var inputString;

function pop(user){
    // create fragment to add in
    var frag = document.createDocumentFragment();

    var contents = frag.appendChild(document.createElement('blockquote'));

    contents = contents.appendChild(document.createElement('p'));
    contents.appendChild(document.createTextNode('Always two there are'));


    //pulls the correct input tag
    var inputTag = document.getElementById('banana');
    
    // grabs the entered value string
    inputString = inputTag.value;
    
    // check to make sure its still linked
    if(user == 1){
        alert(inputString);
    }
    
    // get the right div tag
    var divNeeded = document.getElementById("add-messages");

    divNeeded.appendChild(frag);

    // the intro to each message added into the chat conversation
    var introString = '<li class="media"><div class="media-body"><div class="media">';

    // the header for the next part of the html chunk is dependent on interviewer or candidate
    var interviewer = '<a class="pull-left" href="#"><img class="media-object img-circle " src="../bootstrap-chat-example/assets/img/interviewer.png" /></a><div class="media-body" >';
    var candidate = '<a class="pull-left" href="#"><img class="media-object img-circle " src="../bootstrap-chat-example/assets/img/cat.png" /></a><div class="media-body" >';
    
    // closing tags
    var endingString = '</div></div></div></li>';

    // yay javascript just uses + signs to add things together
    if(user == 0){
        var htmlToAdd = introString + interviewer + inputString + endingString;
    }
    else if (user == 1){
        var htmlToAdd = introString + candidate + inputString + endingString;
    }
    else{
        alert('yo you fucked up')
    }

    divNeeded.appendChild(document.createElement('div'));
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

