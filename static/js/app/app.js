//http://www.adequatelygood.com/JavaScript-Module-Pattern-In-Depth.html
//https://toddmotto.com/mastering-the-module-pattern/
var app = (function () {
    var app = {};

    app.submitGuess = function (btn, form, correct_id) {
        var btn = $(btn);
        var form = $(form);

        function s(bc1) {
            btn.css('backgroundColor', bc1);
            setTimeout(function () {
                //btn.css('backgroundColor', bc2);
                //btn.html(text);
                //http://stackoverflow.com/questions/4605671/jquery-submit-doesnt-include-submitted-button
                btn.appendTo(form);
                form.submit();
            }, 500);
        }

        s(correct_id == btn.val() ? "#00ff00" : "#ff0000");
    };

    return app;
}()
    );