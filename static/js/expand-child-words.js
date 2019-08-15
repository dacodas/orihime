function is_definition(node)
{
    return node.tagName == "DIV" && node.className == "definition";
}

function is_reading(node)
{
    return node.tagName = "DIV" && node.className == "reading";
}

let toggle_sibling_paragraphs_display =
    function (event)
{
    for ( let node of this.parentElement.childNodes )
        if ( is_definition(node) )
            node.style.display = node.style.display == "block" ? "none" : "block";
}

let words = document.getElementsByClassName("orihime-word");

function hide_words_and_set_onclick() 
{
    for ( let word of words )
        for ( let node of word.childNodes )
    {
        if ( is_reading(node) )
            node.onclick = toggle_sibling_paragraphs_display;

        if ( is_definition(node) )
            node.style.display = "none";
    }
}

hide_words_and_set_onclick()

let definitions = []

for ( let word of words )
{
    for ( let node of word.childNodes )
    {
        if ( is_definition(node) )
            definitions.push(node.innerHTML)
    }
}

function toggle_definition(word_number)
{
    for ( let node of words[word_number].childNodes )
    {
        if ( is_definition(node) )
        {
            node.innerHTML = node.innerHTML == '[...]' ? definitions[word_number] : '[...]';
        }
    }
}
