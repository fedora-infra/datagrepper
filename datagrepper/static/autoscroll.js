$(document).ready(function(){
    function getUrlVars() {
        var vars = {}, hash;
        var hashes = window.location.search.slice(1).split('&');
        for(var i = 0; i < hashes.length; i++) {
            hash = hashes[i].split('=');
            if (vars[hash[0]] === undefined) { vars[hash[0]] = [];}
            vars[hash[0]].push(hash[1]);
        }
        return vars;
    }

    var _request_in_progress = false;
    var param = getUrlVars();
    if (param.page === undefined) {param.page = 1;}
    var _page = parseInt(param.page);  // Hang on to that..

    var margin = 100;

    function autoscroll(){
        if ($(window).scrollTop() + margin >= $(document).height() - $(window).height()){
            if (_request_in_progress) { return; }
            _request_in_progress = true;
            $("#loader").removeClass('hidden');
            var param = getUrlVars();
            _page = _page + 1;
            param.page = _page;
            param.chrome = 'false';
            $.ajax({
                url: window.location.pathname,
                data: $.param(param, traditional=true),
                dataType: 'html',
                success: function(html){

                    $("#loader").addClass('hidden');
                    _request_in_progress = false;

                    if (html.length == 0) {
                        // Then this is the last page.  Stop.
                        return;
                    }

                    $("#message-container").append(html);
                    autoscroll();
                }
            });
        }
    };
    $(window).scroll(autoscroll);
    autoscroll();
});
