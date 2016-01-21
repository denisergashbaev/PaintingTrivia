//http://www.adequatelygood.com/JavaScript-Module-Pattern-In-Depth.html
//https://toddmotto.com/mastering-the-module-pattern/

var app = (function () {
    var app = {};

    app.submitGuess = function (btn, form, correct_id) {
        var btn = $(btn);
        var form = $(form);
        //create hidden el: http://stackoverflow.com/questions/2408043/jquery-create-hidden-form-element-on-the-fly
        // extend form
        $('<input>').attr({
            type: 'hidden',
            name: btn.prop('name'),
            value: btn.val()
        }).appendTo(form);
        function s(bc) {
            btn.css('backgroundColor', bc);
            setTimeout(function () {
                form.submit();
            }, 500);
        }

        s(correct_id == btn.val() ? "#00ff00" : "#ff0000");
    };

    return app;
}()
    );