// As a general reference
// https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener#The_value_of_this_within_the_handler

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

// This appears to be currently broken
function update_definition()
{
    let xpath = "//div[@id=\"orihime-text-tree\"]/div[@class=\"definition\"]"
    let main_text_div = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE).singleNodeValue
    let text_hash = main_text_div.id

    let selection = window.getSelection()

    function reqListener () {
        console.log(this.responseText);
        result = document.evaluate("//div[@id=\"orihime-text-tree\"]", document);
        result.iterateNext().innerHTML = this.responseText;
        hide_words_and_set_onclick();
    }

    var csrftoken = getCookie('csrftoken');
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", reqListener);
    oReq.open("POST", "/_text-tree/" + text_hash);
    oReq.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    oReq.setRequestHeader("X-CSRFToken", csrftoken);
    oReq.send()
}

// Switch on backend selection
function search_for_selection()
{
    var search_request = new XMLHttpRequest();
    search_request.open("POST", "/search/goo/" + orihime_selection.reading, false);
    // search_request.open("POST", "/search/larousse/" + orihime_selection.reading, false);
    search_request.addEventListener("load", handle_search_response);
    search_request.send();
}

function handle_search_response(event)
{
    search_request = this

    var div = document.createElement("div");
    div.id = "overlay";

    div.innerHTML = "<div class=\"word-selection\"><ul>" + search_request.responseText + "</ul></div>";
    document.body.appendChild(div)

    // 1. Append child
    // 2. Count number of list items in new element
    // 3. Only go through UI with user if there are more than one

    search_items = document.evaluate("//*[@id=\"overlay\"]/div/ul/li", div)

    var search_item = search_items.iterateNext(); 
    while (search_item)
    {
        console.log("Adding a click event");
        search_item.addEventListener("click", handle_search_result_click)
        search_item = search_items.iterateNext();
    }
}

function handle_search_result_click(event)
{
    let list_item = this;

    let header = document.evaluate("./h1", list_item, null, XPathResult.FIRST_ORDERED_NODE_TYPE).singleNodeValue
    let reading = header.innerText

    let definition_div = document.evaluate("./div[@class=\"definition\"]", list_item, null, XPathResult.FIRST_ORDERED_NODE_TYPE).singleNodeValue
    let definition = definition_div.innerHTML

    console.log("You clicked a search result");
    console.log("Reading: " + reading);
    console.log("Definition: " + definition);

    let overlay_div = document.evaluate("//div[@id=\"overlay\"]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE).singleNodeValue
    overlay_div.remove()

    add_child_word(reading, definition, orihime_selection.text_hash)
}

function add_child_word(reading, definition, text_hash)
{
    body = {
        "reading": reading,
        "definition": definition,
        "text": text_hash,
        "begin": 5,
        "end": 10
    }

    var csrftoken = getCookie('csrftoken');
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", update_definition);
    oReq.open("POST", "/_word-relations/");
    oReq.setRequestHeader("Content-Type", "application/json");
    oReq.setRequestHeader("X-CSRFToken", csrftoken);
    oReq.send(JSON.stringify(body));
}

function OrihimeSelection()
{
    this.selection = null
    this.text_hash = null
    this.ocurrence = null
    this.reading = null
    this.state = "invalid"

    this.set_selection = function (selection)
    {
        this.selection = selection;

        if ( selection.anchorNode != null )
        {
            this.text_hash = selection.anchorNode.parentElement.closest("div.definition").id;
            this.ocurrence = selection.toString();
            this.reading = this.ocurrence;
            this.state = "valid";
        }
    }

    this.clear_selection = function ()
    {
        this.selection = null
        this.state = "invalid"
    }
}

// A global
var orihime_selection = new OrihimeSelection()

// Trying to get the highlighted text via window.getSelection on
// mouseDown or onClick doesn't work, as the highlight is deselected
// on mousedown. Hence, this function
function setup_add_button()
{
    let result = document.evaluate("//div[@id=\"add-button\"]", document)
    add_button = result.iterateNext()

    // Use event listeners instead here?
    add_button.onmouseenter = (function ()
                        {
                            let window_selection = window.getSelection();
                            orihime_selection.set_selection(window_selection);
                        });
    add_button.onmouseleave = (function ()
                        {
                            orihime_selection.clear_selection();
                        });
    add_button.onmousedown = search_for_selection;
    add_button.onclick = null;
}

setup_add_button()
