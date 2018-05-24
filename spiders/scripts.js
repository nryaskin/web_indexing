Array.prototype.last = function () {
    return this[this.length - 1];
};
String.prototype.last = function () {
    return this[this.length - 1];
};

// Init section
$(document).ready(function () {
    const app = new App();

    $('#search-app').on('click', function(e){
        if(app.lastInput === '#word-app'){
            app.getRequest('/urls', '#word-app', App.onWordTyping, app);
        }else{
            app.getRequest('/words', '#url-app', App.onLinkTyping, app);
        }
        e.preventDefault();
    });

    $('#word-app').keyup(function () {
        app.lastInput = '#word-app';

    });

    $('#url-app').keyup(function () {
        app.lastInput = '#url-app';
    });
});

class App {
    constructor() {
        this.wordsResult = [];
        this.linksResult = [];
        this.lastCalledMethod = undefined;
        this.lastInput = undefined;
    }

    onTyping(array, method) {
        // Fuck javascript
        let previousContainer = method === 'link' ? this.linksResult : this.wordsResult;
        let searchContainer = $('#searchResult-app');
        if(this.lastCalledMethod !== method){
            $(searchContainer).empty();
        }
        this.lastCalledMethod = method;
        let difference = _.difference(array, previousContainer);
        let resultContainer = $(searchContainer);
        if (difference.length > 0) {
            _.each(difference, function (item) {
                if(method === 'link'){
                    let element = $(`<li class="list-group-item" id="${item}"><a href="${item}">${item}</a></li>`);
                    $(resultContainer).prepend(element);
                }
                else{
                    let element = $(`<li class="list-group-item" id="${item}">${item}</li>`);
                    $(resultContainer).prepend(element);
                }
            });
        }
        else {
            difference = _.difference(previousContainer, array);
            _.each(difference, function (item) {
                // Doing this weird stuff because we have unrecognized by jQuery engine characters inside URL
                $(document.getElementById(item)).remove();
            });
        }
        // Fuck javascript
        if(method === 'link')
            this.linksResult = array;
        else
            this.wordsResult = array;
    }

    static onWordTyping(data, instance) {
        instance.onTyping(data.links, 'word');
    }

    static onLinkTyping(data, instance) {
        instance.onTyping(data.words, 'link');
    }

    getRequest(url, idSelector, callback, appInstance) {
        let val = $(idSelector).val();
        $('#form-app').block({message: null});
        $.get({
            url: url, data: {'values': val}, success: function (response) {
                callback(response, appInstance);
            }, complete:function(){
                $('#form-app').unblock();
            }
        });
    }
}