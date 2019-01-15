## Insert Randomized List Add-on for Anki

<!-- MarkdownTOC -->

- [Installation Guide](#installation-guide)
    - [Installing JS Booster](#installing-js-booster)
    - [Installing the card template](#installing-the-card-template)
    - [Installing the Add-on](#installing-the-add-on)
- [Usage](#usage)
    - [Adding a randomized list](#adding-a-randomized-list)
    - [Randomizing all lists in a template](#randomizing-all-lists-in-a-template)
    - [Add-on compatibility](#add-on-compatibility)

<!-- /MarkdownTOC -->


### Installation Guide

Two dependencies have to be set-up before using this add-on:

1. The [JS Booster](https://ankiweb.net/shared/info/1280253613) add-on (Anki
   2.0) **OR** the [Cookie Monster](https://ankiweb.net/shared/info/1501583548)
   add-on (Anki 2.1), and
2. A special JavaScript snippet that allows for list randomization in your templates

#### Installing JS Booster / Cookie Monster

Both JS Booster (on Anki 2.0) and Cookie Monster (on Anki 2.1) include a few modifications that bring Anki desktop in line with AnkiDroid in terms of its JavaScript support. This is important for the list randomization to work correctly, as it depends on cookies to preserve the list state across front and back of your cards.

**Anki 2.0**

You can install JS Booster from [this link](https://ankiweb.net/shared/info/1280253613). Support for the browser preview window can be added by installing [this complementary add-on](https://ankiweb.net/shared/info/19206336).

**Anki 2.1**

You can grab the Cookie Monster add-on [here](https://ankiweb.net/shared/info/1501583548).

#### Installing the card template

From Anki's main window, please head to *Tools* –> *Manage Note Types* and find the note type you want to enable list randomization on (e.g. *Cloze*). Proceed by clicking on *Cards* to invoke the card template editor.

Please now apply the following changes:

1. Wrap the contents of the *Front Template* field with `<div id="front">CONTENTS HERE</div>`. E.g. for the cloze template:

        <div id="front">
        {{cloze:Text}}
        </div>

2. Copy and paste the contents of [template.html](template.html) at the end of both the *Front Template* and *Back Template* of your cards.

Here is how the results should look for the *Cloze* note type:

*Front Template*

    <div id="front">
    {{cloze:Text}}
    </div>

    <script>
    var createCookie = function(name, value, days) {
        var expires;
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toGMTString();
        }
        else {
            expires = "";
        }
        document.cookie = name + "=" + value + expires + "; path=/";
    }

    function getCookie(c_name) {
        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) {
                    c_end = document.cookie.length;
                }
                return unescape(document.cookie.substring(c_start, c_end));
            }
        }
        return "";
    }

    function getRandomElms(){
        var ul = document.querySelectorAll('ul.shuffle');
        return ul
    }

    function getRandArr(elm, array){
        for (var i = elm.children.length; i >= 0; i--) {
            rand = Math.random() * i | 0;
            array.push(rand)
        }
    }

    function shuffleWithArr(elm, array){
        elm.style.backgroundColor = "inherit"
        for (var i = elm.children.length; i >= 0; i--) {
            elm.appendChild(elm.children[array[i]]);
        }
    }

    function run() {
        var elms = getRandomElms()
        var isFront = document.getElementById("front");

        for (var i = 0; i < elms.length; i++) {
            var idxArr = [];
            elm = elms[i]
            if (isFront) {
                getRandArr(elm, idxArr);
                // convert idxArr array to a JSON string to be stored
                var json_str = JSON.stringify(idxArr);

                // persist the idxArr order and correct answers
                createCookie('idxArr' + i, json_str);

                var stored_data = idxArr
            } else {
                // get the idxArr order
                var json_data = getCookie('idxArr' + i);
                // get the array back from storage
                var stored_data = JSON.parse(json_data);
            }
            shuffleWithArr(elm, stored_data)
        }
    }

    run();

    </script>


*Back Template*

    {{cloze:Text}}<br>
    {{Extra}}

    <script>

    var createCookie = function(name, value, days) {
        var expires;
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toGMTString();
        }
        else {
            expires = "";
        }
        document.cookie = name + "=" + value + expires + "; path=/";
    }

    function getCookie(c_name) {
        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) {
                    c_end = document.cookie.length;
                }
                return unescape(document.cookie.substring(c_start, c_end));
            }
        }
        return "";
    }

    function getRandomElms(){
        var ul = document.querySelectorAll('ul.shuffle');
        return ul
    }

    function getRandArr(elm, array){
        for (var i = elm.children.length; i >= 0; i--) {
            rand = Math.random() * i | 0;
            array.push(rand)
        }
    }

    function shuffleWithArr(elm, array){
        elm.style.backgroundColor = "inherit"
        for (var i = elm.children.length; i >= 0; i--) {
            elm.appendChild(elm.children[array[i]]);
        }
    }

    function run() {
        var elms = getRandomElms()
        var isFront = document.getElementById("front");

        for (var i = 0; i < elms.length; i++) {
            var idxArr = [];
            elm = elms[i]
            if (isFront) {
                getRandArr(elm, idxArr);
                // convert idxArr array to a JSON string to be stored
                var json_str = JSON.stringify(idxArr);

                // persist the idxArr order and correct answers
                createCookie('idxArr' + i, json_str);

                var stored_data = idxArr
            } else {
                // get the idxArr order
                var json_data = getCookie('idxArr' + i);
                // get the array back from storage
                var stored_data = JSON.parse(json_data);
            }
            shuffleWithArr(elm, stored_data)
        }
    }

    run();

    </script>


Please note that the JS script above might change over time (as a result of updates, etc.). Make sure to always use the code in template.html for the most recent version of the script.


#### Installing the Add-on

Having performed all of the changes above you can then proceed to install the add-on itself by either moving `anki-editor-random-list.py` into your Anki add-on directory (*Tools* –> *Add-ons* –> *Open Add-ons folder*) or by installing the add-on from [AnkiWeb](https://ankiweb.net/shared/info/1280092568).

### Usage

#### Adding a randomized list

Having installed the add-on, a new toolbar button should appear in your Anki editor screen. If you push this button or use its keyboard shortcut (<kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>L</kbd>) the add-on will insert an unordered list with a `shuffle` CSS class into the current field. While reviewing your cards, lists with this class will be identified by the embedded JavaScript code in your template and randomized in a consistent manner across back and front.

In order to be able to tell randomized lists apart from regular lists they will appear with a yellow background in the editor window. This color won't appear when actually reviewing your cards.

#### Randomizing all lists in a template

If you'd like to have all of your unordered lists randomized, regardless of whether or not you created them using the add-on button, you can modify the JavaScript snippet you inserted into your templates and replace `ul.shuffle` in `getRandomElms` with `ul`.

#### Add-on compatibility

The lists generated by this add-on should be compatible with Anki and AnkiDroid. I have not tested this with AnkiWeb or AnkiMobile.