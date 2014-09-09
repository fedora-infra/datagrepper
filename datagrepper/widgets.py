""" Contains code for producing embeddable widgets """

import flask
from datagrepper.app import app


js_helpers = """
function include_js(url, success) {
    var script     = document.createElement('script');
    script.src = url;

    var head = document.getElementsByTagName('head')[0],
    done = false;
    // Attach handlers for all browsers
    script.onload = script.onreadystatechange = function() {
        if (!done && (
                !this.readyState ||
                this.readyState == 'loaded' ||
                this.readyState == 'complete'
                )) {
            done = true;
            success();  // Do the callback
            script.onload = script.onreadystatechange = null;
            head.removeChild(script);  /* poof */
        };
    };
    head.appendChild(script);
};

function run_with_jquery(callback) {
    var jq_url = '%(base)s/static/jquery-2.1.0.min.js'
    if (typeof jQuery == 'undefined') {
        include_js(jq_url, callback);
    } else {
        callback();
    }
}"""

work = """
var datagrepper_success = function(json) {
    $.each(json.raw_messages, function(i, msg) {
        var meta = msg.meta;
        if (meta === undefined) { meta = msg; }
        var card = '<div class="message-card">';
        if (meta.icon) {
            if (meta.link) {
                card = card +
                    '<a href="' + meta.link + '">' +
                    '<img src="' + meta.icon + '"/>' +
                    '</a>';
            } else {
                card = card + '<img src="' + meta.icon + '"/>';
            }
        }
        if (meta.secondary_icon) {
            card = card +
                '<img src="' + meta.secondary_icon + '"/>';
        }
        card = card +
            '<p>' + meta.subtitle + '</p>' +
            '</div>';
        card = card + '<div class="datetime">' + meta['date'] + '</div>';
        $("div#datagrepper-widget").append(card);
    });
}

// These are the default arguments that we use for our datagrepper query
var data = {
    order: 'desc',
    chrome: 'false'
};

// Check to see if the user has asked us to filter the firehose.
var datagrepper_attrs = [
    'user', 'package', 'category', 'topic',
    'order', 'rows_per_page', 'page', 'size',
    'grouped'];
$.each(datagrepper_attrs, function(i, attr) {
    var value = $('script#datagrepper-widget').attr("data-" + attr);
    if (value != undefined) {
        data[attr] = value;
    }
});

$.ajax(
    '%(base)s/raw/?meta=link&meta=icon' +
    '&meta=secondary_icon&meta=subtitle&meta=date', {
        data: data,
        dataType: 'jsonp',
        success: datagrepper_success,
        error: function() {
            console.log(arguments);
        }
    }
)
"""

css_helper = """
$('head').append('<link rel="stylesheet" href="%s" type="text/css"/>');
"""


@app.route('/widget.js')
def widget_js():
    """ This code is super ugly.
    But it produces a widget as a self-extracting script.

    """

    prefix = flask.request.url_root[:-1]

    raw_widget = '<div id="datagrepper-widget"></div>'
    scripts, calls, css = [], [work % dict(base=prefix)], []

    if flask.request.args.get('css', '').lower() == 'true':
        def static_url(filename):
            return app.config['APP_PATH'] + "/static/" + filename

        css.append(css_helper % static_url('css/bootstrap.css'))
        css.append(css_helper % static_url('css/raw.css'))

    # This, ridiculously, will find the place in the DOM of the script tag
    # responsible for running this javascript at the time of its execution.
    # This allows us to inject our graph in-place; i.e., wherever the user
    # includes our tag, that's where the graph will unpack itself.
    calls.insert(0, "$('script#datagrepper-widget').before('%s');" % raw_widget.strip())
    calls.extend(css)

    # Just for debugging...
    #calls.append("console.log('waaaaaat!');")
    inner_payload = ";\n".join(calls)

    envelope = inner_payload
    for script in reversed(scripts):
        envelope = """$.getScript("%s", function(){%s});""" % (
            prefix + script, envelope)

    body = js_helpers % dict(base=prefix)
    body += "\nrun_with_jquery(function() {%s});" % envelope

    return flask.Response(
        response=body,
        status=200,
        mimetype='application/javascript',
    )
