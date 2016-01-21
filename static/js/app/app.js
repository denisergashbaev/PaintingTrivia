//http://www.adequatelygood.com/JavaScript-Module-Pattern-In-Depth.html
//https://toddmotto.com/mastering-the-module-pattern/

var app = (function () {
    var app = {};
    app.submitGuess = function (btn, correct_id) {
        var btn = $(btn)

        // Create a new form
        var form = $(document.createElement('form'));
        $(form).attr("method", "POST");
        var input = $("<input>").attr("type", "hidden").attr("name", btn[0].name).val(btn.val());
        $(form).append($(input));
        function s(bc1) {
            btn.css('backgroundColor', bc1);
            setTimeout(function () {$(form).submit();},500);
        }
        s(correct_id == btn.val() ? "#00ff00" : "#ff0000");
        return false;
    };
    return app;
}()
    );