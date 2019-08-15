var highlighted_selection = null

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function update_definition()
{
    let result = document.evaluate("//div[@id=\"orihime-text\"]/div[@class=\"definition\"]", document)
    let text_hash = result.iterateNext().id

    let selection = window.getSelection()

    function reqListener () {
        console.log(this.responseText);
        result = document.evaluate("//div[@id=\"orihime-text\"]", document);
        result.iterateNext().innerHTML = this.responseText;
        hide_words_and_set_onclick();
    }

    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", reqListener);
    oReq.open("POST", "/_text-tree/" + text_hash);
    oReq.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    oReq.send()
}

function search_word(reading)
{
    var csrftoken = getCookie('csrftoken');

    function add_word()
    {
        body = {
            "reading": reading,
            "definition": this.responseText
        }

        var oReq = new XMLHttpRequest();
        oReq.open("POST", "/words/");
        oReq.setRequestHeader("Content-Type", "application/json");
        oReq.setRequestHeader("X-CSRFToken", csrftoken);
        oReq.send(JSON.stringify(body));
    }

    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", add_word);
    oReq.open("POST", "/search/" + reading, false);
    oReq.send();

    return oReq.responseText;
}

function add_child_word()
{
    // Trying to get the highlighted text via window.getSelection on
    // mouseDown or onClick doesn't work, as the highlight is
    // deselected on mousedown

    // let selection = window.getSelection()
    let selection = highlighted_selection

    let text_hash = selection.anchorNode.parentElement.id;
    let ocurrence = selection.toString();
    let reading = ocurrence;

    search_word(reading)

    function reqListener () {
        console.log(this.responseText);
        update_definition();
    }

    body = {
        "text": text_hash,
        "word": reading,
        // "ocurrence": ocurrence
        "begin": 5,
        "end": 10
    }

    var csrftoken = getCookie('csrftoken');
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", reqListener);
    oReq.open("POST", "/_word-relations/");
    oReq.setRequestHeader("Content-Type", "application/json");
    oReq.setRequestHeader("X-CSRFToken", csrftoken);
    oReq.send(JSON.stringify(body));
}

{
    let result = document.evaluate("//div[@id=\"add-button\"]", document)
    add_button = result.iterateNext()
    add_button.onmouseenter = (function ()
                        {
                            highlighted_selection = window.getSelection();
                        });
    add_button.onmouseleave = (function ()
                        {
                            highlighted_selection = null;
                        });
    add_button.onmousedown = add_child_word;
    add_button.onclick = null;
}
