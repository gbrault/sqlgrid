.. sqlgrid documentation master file, created by
   sphinx-quickstart on Tue Sep  1 11:25:28 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: https://media.quantopian.com/logos/open_source/sqlgrid-logo-03.png
    :target: https://sqlgrid.readthedocs.io
    :width: 190px
    :align: center
    :alt: sqlgrid

sqlgrid API Documentation
=======================

sqlgrid is a Jupyter notebook widget which uses `SlickGrid <https://github.com/mleibman/SlickGrid>`_ to render pandas
DataFrames within a Jupyter notebook. This allows you to explore your DataFrames with intuitive scrolling, sorting, and
filtering controls, as well as edit your DataFrames by double clicking cells.

sqlgrid was developed for use in `Quantopian's hosted research environment
<https://www.quantopian.com/posts/sqlgrid-now-available-in-research-an-interactive-grid-for-sorting-and-filtering-dataframes?utm_source=readthedocs&utm_medium=web&utm_campaign=sqlgrid-repo>`_
and is available for use in that environment as of June 2018.


Other sqlgrid resources
---------------------

This page hosts only the API docs for the project.  You might also be interested in these other sqlgrid-related
resources:

`sqlgrid on GitHub <https://github.com/quantopian/sqlgrid>`_
  This is where you'll find the source code and the rest of the documentation for the project, including the
  instructions for installing and running sqlgrid.

`sqlgrid demo on Quantopian <https://www.quantopian.com/clone_notebook?id=5ae9cff15230100046c3958d&utm_source=readthedocs&utm_medium=web&utm_campaign=sqlgrid-repo>`_
  Click the badge below try out the latest beta of sqlgrid in Quantopian's hosted research environment. If you're
  already signed into Quantopian you'll be brought directly to the demo notebook. Otherwise you'll be prompted
  to register (it's free):

  .. image:: https://img.shields.io/badge/launch-quantopian-red.svg?colorB=d33015
    :target: https://www.quantopian.com/clone_notebook?id=5b2baee1b3d6870048620188&utm_source=github&utm_medium=web&utm_campaign=sqlgrid-repo

`sqlgrid demo on binder <https://beta.mybinder.org/v2/gh/quantopian/sqlgrid-notebooks/master?filepath=index.ipynb>`_
  Click the badge below or the link above to try out sqlgrid using binder.  You'll see a brief loading screen and
  then a notebook will appear:

  .. image:: https://beta.mybinder.org/badge.svg
    :target: https://beta.mybinder.org/v2/gh/quantopian/sqlgrid-notebooks/master?filepath=index.ipynb


:mod:`sqlgrid` Module
-------------------

.. automodule:: sqlgrid
    :members:
    :exclude-members: sqlgridWidget

    .. autoclass:: sqlgridWidget(df=None, grid_options=None, precision=None, show_toolbar=None)
        :members:
