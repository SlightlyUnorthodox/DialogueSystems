function create(htmlStr) {
    var frag = document.createDocumentFragment(),
        temp = document.createElement('div');
    temp.innerHTML = htmlStr;
    while (temp.firstChild) {
        frag.appendChild(temp.firstChild);
      }
        return frag;
    }

    var fragment = create('<div class="someclass"><a href="www.example.com"><p>some text</p></a></div>'); 

    document.body.insertBefore(fragment, document.body.childNodes[0]);
