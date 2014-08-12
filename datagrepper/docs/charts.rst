Charts and Graphs
=================

Datagrepper provides a wide-array of charts in SVG format that you can use to
visualize message history in your blog, website, or application.

Usage
-----

You simply include an ``<img>`` tag with the ``src`` pointed at the `charts URL
<charts/line>`_, like this::

    <html>
      <body>
        <h1>My Site</h1>
        <p class="lead">Welcome to my site.</p>
        <p>Here is a comparison of activity on the kernel, dracut, and systemd packages:</p>

        <img src="https://apps.fedoraproject.org/datagrepper/charts/line?package=kernel&package=systemd&package=dracut&split_on=packages"/>

        <footer>Happy Hacking!</footer>
      </body>
    </html>

Options
-------

There are **lots** of options.

First, you can specify all the same options that you would to 'raw' queries.
The the documentation on the main page for more information about those.  You
can filter by ``user``, ``package``, ``category``, and ``topic`` (as well as
``not_user``, ``not_package``, etc..).

Per User
~~~~~~~~

Using a url like ``charts/line?user=remi`` will give you a chart like this:

.. image:: http://localhost:5000/charts/line?user=remi&height=300&title=Activity%20for%20user%20%22remi%22

Per Package
~~~~~~~~~~~

Or you could produce graphs specific to a package with a url like ``charts/line?package=nethack``:

.. image:: http://localhost:5000/charts/line?package=nethack&height=300&title=Fedora%20activity%20for%20the%20nethack%20package

Per Category
~~~~~~~~~~~~

Following along the same theme, you could limit your graph to only
displaying the count of messages from a particular subsystem.  For
instance, the graph at ``charts/line?category=buildsys`` shows the trend
of activity in the koji build system:

.. image:: http://localhost:5000/charts/line?category=buildsys&height=300&title=Koji

Combining all that
~~~~~~~~~~~~~~~~~~

Just like with normal queries to the JSON API, you can combine query
types like showing only koji messages for the kernel, dracut, and systemd
packages with
``charts/line?package=kernel&package=dracut&package=systemd&category=buildsys``:

.. image:: http://localhost:5000/charts/line?package=kernel&package=dracut&package=systemd&category=buildsys&height=300&title=Koji

Chart Types
-----------

So far you have only seen the ``charts/line`` URL, but there are many
others.  Choose from any of these:

- line
- stackedline
- xy
- bar
- horizontalbar
- stackedbar
- horizontalstackedbar
- funnel
- pyramid
- verticalpyramid
- dot
- gauge

For example, here is ``charts/bar?category=wiki``:

.. image:: http://localhost:5000/charts/bar?category=wiki&height=300&title=Wiki%20Activity

Styles
------

All the graphs above have been in the ``default`` style, but you can specifify different ones:

The full list is:

- blue
- turquoise
- neon
- dark_green
- dark_solarized
- dark_green_blue
- dark_colorized
- default
- light
- light_colorized
- light_solarized
- green
- clean
- light_red_blue

Check it out.. here's ``charts/horizontalbar?category=fedoratagger&style=light_solarized``:

.. image:: http://localhost:5000/charts/horizontalbar?category=fedoratagger&height=300&style=light_solarized&title=Fedora%20Tagger

Splitting Series
----------------

In the kernel/dracut/systemd example above, it might be nice to split those out
into independent series.  You can do that with the ``split_on`` parameter.

``charts/line?package=kernel&package=dracut&package=systemd&split_on=packages``:

.. image:: http://localhost:5000/charts/line?package=kernel&package=dracut&package=systemd&split_on=packages&height=300

You can also split on multiple kinds of factors at once:

.. image:: http://localhost:5000/charts/line?package=kernel&package=dracut&package=systemd&split_on=packages&category=buildsys&category=git&split_on=categories&height=300

Other options
-------------

- ``title``, Set a title on the plot.

.. image:: http://localhost:5000/charts/line?height=300&title=Just%20an%20example%20title

- ``N``, (int), the number of data points in the graph (the resolution of
  the x-axis).

.. image:: http://localhost:5000/charts/line?N=3&height=300&title=With%20N=3

- ``width``, (int), Defaults to ``800``.  Sets the width of the plot in pixels.
- ``height``, (int), Defaults to ``600``.  Sets the height of the plot in pixels.

- ``interpolation``, (boolean), Defaults to ``None``. You can also pass it
  ``cubic`` or ``quadratic``.

.. image:: http://localhost:5000/charts/line?interpolation=cubic&height=300&title=Cubic%20Interpolation

- ``human_readable``, (boolean), Defaults to ``True``.  Converts numbers to
  nicer-to-read numbers.

.. image:: http://localhost:5000/charts/line?human_readable=False&height=300&title=Less%20readable,%20maybe..

- ``logarithmic``, (boolean), Defaults to ``False``.  Logarithmically scales
  the y-axis.

.. image:: http://localhost:5000/charts/line?logarithmic=True&height=300&title=Logarithmic

- ``show_x_labels``, (boolean), Defaults to ``True``.  Show/hide the x-axis
  labels.
- ``show_y_labels``, (boolean), Defaults to ``True``.  Show/hide the y-ayis
  labels.

.. image:: http://localhost:5000/charts/line?show_x_labels=False&show_y_labels=False&height=300&title=Sans%20labels

- ``show_dots``, (boolean), Defaults to ``True``.  Show/hide the datapoints.

.. image:: http://localhost:5000/charts/line?show_dots=False&height=300&title=Hidden%20dots

- ``fill``, (boolean), Defaults to ``False``.  Fill the area under curves in
  line plots.

.. image:: http://localhost:5000/charts/stackedline?fill=True&height=300&title=Area%20under%20the%20curve
