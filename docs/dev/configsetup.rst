Config setup
============

.. graphviz::

   digraph loadmodule {
      a [label="On deamon start"]
      b [label="Load config file", shape="rect"];
      c [label="Overwrite config file with environment variables", shape="rect"]
      d [label="Overwrite the result with command line arguments", shape="rect"]
      e [label="Add modules directories to python path", shape="rect"]

      a -> b -> c -> d -> e ;
   }

This is done by ``app.config`` module.
