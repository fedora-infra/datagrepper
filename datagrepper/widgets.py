""" Contains code for producing embeddable widgets """

import flask
from datagrepper.app import app


def intify(value):
    try:
        return int(value)
    except ValueError:
        return value


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

socket = """
var datagrepper_success = function(json) {
    $.each(json.raw_messages, function(i, msg) {
        var meta = msg.meta;
        var card = '<div class="message-card">';
        card = card +
            '<a href="' + meta.link + '">' +
            '<img src="' + meta.icon + '"/>' +
            '</a>';
        card = card +
            '<img src="' + meta.secondary_icon + '"/>';
        card = card +
            '<p>' + meta['subtitle'] + '</p>' +
            '</div>';
        card = card + '<div class="datetime">' + meta['date'] + '</div>';
        $("#datagrepper-widget").append(card);
    });
}
$.ajax(
    '%(base)s/raw/', {
        data: {
            order: 'desc',
            chrome: 'false',
            meta: 'link',
            meta: 'icon',
            meta: 'secondary_icon',
            meta: 'subtitle',
            meta: 'date'
        },
        dataType: 'jsonp',
        success: datagrepper_success,
        error: function() {
            console.log(arguments);
        }
    }
)
console.log('socket goes here')
"""

css_helper = """
$('head').append('<link rel="stylesheet" href="%s" type="text/css"/>');
"""


@app.route('/widget.js')
def widget_js():
    """ This code is super ugly.
    But it produces a widget as a self-extracting script.

    It can take some parameters to change the shape and character of the
    chart.

    It renders the chart widget and the moksha socket, strips any boilerplate
    html, grabs all the resources and then builds a single javascript blob that
    dynamically loads the resources before finally calling the
    moksha_socket and widget javascript.

    It takes the boilerplate html that it stripped and
    dynamically injects it back into the host page.

    """

    defaults = {
        'width': 960,
        'height': 75,
        'n': 100,
        'duration': 750,
    }

    params = defaults
    params.update(dict([
        (k, intify(v)) for k, v in flask.request.args.items()
    ]))

    prefix = flask.request.url_root[:-1]

    raw_widget = '<div id="datagrepper-widget"></div>'
    scripts, calls, css = [], [socket % dict(base=prefix)], []

    # This, ridiculously, will find the place in the DOM of the script tag
    # responsible for running this javascript at the time of its execution.
    # The "last" script tag on the page during page load is the tag responsible
    # for the code run at that time.  This allows us to inject our graph
    # in-place; i.e., wherever the user includes our tag, that's where the
    # graph will unpack itself.
    calls.insert(0, "$('script:last').before('%s');" % raw_widget.strip())

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
