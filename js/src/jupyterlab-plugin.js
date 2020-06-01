var sqlgrid = require('./index');

var base = require('@jupyter-widgets/base');

/**
 * The widget manager provider.
 */
module.exports = {
  id: 'sqlgrid',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'sqlgrid',
          version: sqlgrid.version,
          exports: sqlgrid
      });
    },
  autoStart: true
};
