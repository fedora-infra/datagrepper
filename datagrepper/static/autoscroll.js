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
            $("#loader").show();
            var param = getUrlVars();
            _page = _page + 1;
            param.page = _page;
            param.chrome = 'false';
            $.ajax({
                url: "raw",
                data: $.param(param, traditional=true),
                dataType: 'html',
                success: function(html){
                    $("#loader").hide();
                    $(".col-md-12").append(html);
                    _request_in_progress = false;
                    autoscroll();
                }
            });
        }
    };
    $(window).scroll(autoscroll);
    autoscroll();
});
