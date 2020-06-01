.. image:: docs/images/grid.png
    :target: https://sqlgrid.readthedocs.io
    :width: 80px
    :align: center
    :alt: sqlgrid

=======
sqlgrid
=======
sqlgrid is a Jupyter notebook widget which uses `SlickGrid <https://github.com/mleibman/SlickGrid>`_ to render SQL Database Tables within a Jupyter notebook. This allows you to explore your Tables with intuitive scrolling, sorting, and
filtering controls, as well as edit your Tables by double clicking cells.

sqlgrid is developed as a fork from `Quantopian's QGrid`.

The backend is completly rewrite to supprt SQL table paradygm.

Demo
----

Click the badge below to try out sqlgrid using Jupyter Lab over binder:

.. image:: https://beta.mybinder.org/badge.svg
    :target: https://mybinder.org/v2/gh/seadev/sqlgrid-notebooks/master?urlpath=lab


*For both binder links, you'll see a brief loading screen while a server is being created for you in the cloud.  This shouldn't take more than a minute, and usually completes in under 10 seconds.*

*The binder demos generally will be using the most recent stable release of sqlgrid, so features that were added in a recent beta version may not be available in those demos.*

API Documentation
-----------------
API documentation is hosted on `readthedocs <http://sqlgrid.readthedocs.io/en/latest/>`_.

Installation
------------

Installing
  
  git clone https://github.com/seadevfr/sqlgrid.git
  cd ./sqlgrid
  python setup.py install
  jupyter labextension install js/

At this point if you run jupyter lab normally with the 'jupyter lab' command, you should be
able to use sqlgrid in notebooks as you normally would.

What's New
----------
