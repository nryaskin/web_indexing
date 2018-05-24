Array.prototype.last = function () {
    return this[this.length - 1];
};
String.prototype.last = function () {
    return this[this.length - 1];
};

// Init section
$(document).ready(function () {
    const app = new App();

    $('#word').keyup(function () {
        app.getRequest('/urls', '#word', App.onWordTyping, app);
    });

    $('#url').keyup(function () {
        app.getRequest('/words', '#url', App.onLinkTyping, app);
    });
});

class App {
    constructor() {
        this.wordsResult = [];
        this.linksResult = [];
        this.lastCalledMethod = undefined;
    }

    onTyping(array, containerRef, method) {
        let searchContainer = $('#searchResult');
        if(this.lastCalledMethod !== method){
            $(searchContainer).empty();
        }
        this.lastCalledMethod = method;
        let difference = _.difference(array, containerRef);
        let resultContainer = $(searchContainer);
        if (difference.length > 0) {
            _.each(difference, function (item) {
                let element = $(`<li class="list-group-item" id="${item}">${item}</li>`)
                $(resultContainer).prepend(element);
            });
        }
        else {
            difference = _.difference(containerRef, array);
            _.each(difference, function (item) {
                // Doing this weird stuff because we have unrecognized by jQuery engine characters inside URL
                $(document.getElementById(item)).remove();
            });
        }
        containerRef = data.words;
    }

    static onWordTyping(data, owner) {
        owner.onTyping(data.links, owner.wordsResult, 'word');
    }

    static onLinkTyping(data, owner) {
        owner.onTyping(data.words, owner.linksResult, 'link');
    }

    getRequest(url, idSelector, callback) {
        $(idSelector).keyup(function () {
            let val = $(idSelector).val();
            $.get({
                url: url, data: {'values': val}, success: function (response) {
                    callback(response);
                }
            });
        });
    }
}