.. image:: ./grid.png
    :target: https://sqlgrid.readthedocs.io
    :width: 80px
    :align: center
    :alt: sqlgrid

=======
sqlgrid
=======
sqlgrid is a Jupyter notebook widget which uses `SlickGrid <https://github.com/mleibman/SlickGrid>`_ to render SQL Database Tables within a Jupyter notebook. This allows you to explore your Tables with intuitive scrolling, sorting, and
filtering controls, as well as edit your Tables by double clicking cells.

sqlgrid is developed as a fork from `Quantopian's QGrid` (June 2020).

.. image:: https://camo.githubusercontent.com/f08ed0448415ad8a2ffe872f4c1f7a2317667318/68747470733a2f2f6d656469612e7175616e746f7069616e2e636f6d2f6c6f676f732f6f70656e5f736f757263652f71677269642d6c6f676f2d30332e706e67
    :target: https://github.com/quantopian/qgrid
    :width: 80px
    :align: center
    :alt: qgrid

The backend is a complete rewrite to support SQL table model.

Demo
----

Click the badge below to try out sqlgrid using Jupyter Lab over binder:

.. image:: https://beta.mybinder.org/badge.svg
    :target: https://mybinder.org/v2/gh/seadev/sqlgrid-notebooks/master?urlpath=lab


*For the binder links, you'll see a brief loading screen while a server is being created for you in the cloud.*

*Notice that features that were added in a recent beta version may not be available in stable release.*

API Documentation
-----------------
API documentation is hosted on `readthedocs <http://sqlgrid.readthedocs.io/en/latest/>`_.

Installation
------------

Currently only source installation is possible

Requires
- python
- tools to compile python
- Yarn installed
- npm installed

installing nodejs with tools might do the job on windows

From a shell in a directory and an environment where Jupyter Lab is installed

.. code-block::

  git clone https://github.com/seadevfr/sqlgrid.git
  cd ./sqlgrid
  python setup.py install   (for windows setupw.py)
  pip install ipywidgets or pip install git+https://github.com/jupyter-widgets/ipywidgets.git
  jupyter labextension install --no-build @jupyter-widgets/jupyterlab-manager
  jupyter labextension install --no-build js/
  jupyter lab clean
  jupyter lab build


At this point if you run jupyter lab normally with the 'jupyter lab' command, you should be
able to use sqlgrid in notebooks as you normally would.
you can change password with `jupyter notebook password`

Documentation
-------------

* Python use Sphinx (install it as a prerequisite)
* Javascript use JSDOC (install it as a prerequisite)

For Python

* Go in the doc directory in a shell
* ./make html
* source in doc/source/index.rst

output files are located in the ./doc/build/html directory

For Javascript

* Go in the js directory
* jsdoc -c conf.json

output files are located in the js/out directory

For the User guide

* install mkdocs 
    * pip install mkdocs
    * weasyprint see: https://weasyprint.readthedocs.io/en/stable/install.html
    * pip install git+https://github.com/squidfunk/mkdocs-material.git
    - mkpdfs:
        company: Sea Dev
        author: Gilbert Brault   
    * pip install git+https://github.com/zhaoterryy/mkdocs-pdf-export-plugin.git@master
    * pip install git+https://github.com/comwes/mkpdfs-mkdocs-plugin.git
* cd sqlgrid_user_guide
* mkdocs serve
* mkdocs gh-deploy


What's New
----------
* 01/06/2020 Refactoring
* 07/06/2020 SQL implementation released
* 08/06/2020 Documentation (python + javascript)
* 11/06/2020 Added chinook Database (https://www.sqlitetutorial.net/sqlite-sample-database/) + voila capability
* 25/07/2020 Added user guide based upon mkdocs