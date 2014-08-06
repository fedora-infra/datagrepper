
$(document).ready(function() {
    var pending_count = 0;

    function getUrlVars() {
        var vars = {}, hash;
        var hashes = window.location.search.slice(1).split('&');
        for(var i = 0; i < hashes.length; i++) {
            hash = hashes[i].split('=');
            if (vars[hash[0]] === undefined) { vars[hash[0]] = []; }
            vars[hash[0]].push(hash[1]);
        }
        return vars;
    }

    function error(jqXHR, status, error) {
        console.log("Error getting hit error with this");
        console.log(jqXHR);
        console.log(status);
        console.log(error);
    }

    function WebSocketSetup(attempts) {
        if ( attempts > 3 ) { return; }

        if ("WebSocket" in window) {
            // Let us open a web socket
            var socket_url = "wss://hub.fedoraproject.org:9939";
            //var socket_url = "wss://209.132.181.16:9939";
            var ws = new WebSocket(socket_url);
            ws.onopen = function(e) {
                // Web Socket is connected, send data using send()
                console.log("ws connected to " + socket_url);
                ws.send(JSON.stringify({topic: '__topic_subscribe__', body: '*'}));
            };
            ws.onmessage = function (evt) {
                pending_count = pending_count + 1;
                $("#messages-pending").html(pending_count + " new messages.")
                $("#messages-pending").parent().parent().parent().removeClass('hidden');
            };
            ws.onclose = function(e){ws=null;};
            ws.onerror = function(e){ws=null;WebSocketSetup(attempts + 1);};
        }
    }

    // Lastly, kick it all off, but only if the user has not specified any
    // special query of any complexity at all.  This is because the problem
    // we're trying to solve here just becomes way too complicated too fast.
    // If the user has a query up for category=bodhi&user=lmacken up at the
    // moment, then how do we decide to increment our counter or not.  Punt!
    if (window.location.search == "") {
        WebSocketSetup(1);

        $("#messages-pending").parent().click(function(evt) {
            var params = getUrlVars();
            params['chrome'] = 'false';
            params['rows_per_page'] = pending_count;
            params = $.param(params, traditional=true);
            pending_count = 0;
            $("#messages-pending").parent().parent().parent().addClass('hidden');
            $.ajax({
                url: window.location.pathname,
                dataType: 'html',
                data: params,
                error: error,
                success: function(html) {
                    // TODO - someday figure out how to smoothly animate these
                    $("#message-container").prepend(html);
                },
            });
        })
    }
});
