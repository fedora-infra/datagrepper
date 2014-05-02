Embeddable Widget
-----------------

Datagrepper provides a self expanding javascript file that you can
use to embed message history in your blog, website, or application.

Usage
-----

You simply include a ``<script>`` tag with the id ``datagrepper-widget`` that
references ``widget.js``.  You can indicate what you would like it to display
by using HTML5 ``data-*`` attributes.  If you don't know what those are, don't
sweat it.  An example is worth a thousand words::

    <html>
      <body>
        <h1>My Site</h1>
        <p class="lead">Welcome to my site.</p>
        <p>Here is my latest Fedora activity:</p>

        <script id="datagrepper-widget"
          src="https://apps.fedoraproject.org/datagrepper/widget.js?css=true"
          data-user="ralph"
          data-rows_per_page="40">
        </script>

        <footer>Happy Hacking!</footer>
      </body>
    </html>


See that script tag in the middle?  The ``src`` attribute points at the URL
that you'll want to copy and paste.  It optionally takes a ``css`` argument on
the end which tells it whether or not to include datagrepper's own css.  You
might, for instance, want to style the datagrepper message using your site's
*own* css, not datagrepper's theme.  To do this you can omit the ``css=True``
argument and then define your own style, like so::

    <style>
        #datagrepper-widget img {
            height: 32px;
            width: 32px;
        }
        #datagrepper-widget .message-card {
            font-style: bold;
            display: inline;
        }
        #datagrepper-widget .datetime {
            font-style: italic;
        }
    </style>


Next comes two ``data-*`` attributes that should look familiar from the
JSON api docs.  The first indicates that the widget should render only
messages relating to the FAS user "ralph".  The second indicates that it
should display the latest 40 messages (or as many as it can find).  You
can specify any of the normal attributes: ``data-user``,
``data-package``, ``data-category``, etc.
