Options parsing
===============

.. graphviz::

   digraph loadmodule {
      a [label="On deamon start"]
      b [label="Load config file", shape="rect"];
      c [label="Overwrite config file with environment variables", shape="rect"]
      d [label="Overwrite the result with command line arguments", shape="rect"]

      a -> b -> c -> d ;
   }

This is done by ``app.config.Conf`` class.
