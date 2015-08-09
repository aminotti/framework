Loading module process
======================

.. graphviz::

   digraph loadmodule {
      a [label="Start daemon"]
      b [label="1. Get local module list", shape="rect"];
      c [label="2. Get installed module list from DB", shape="rect"]
      d [label="Upgrade module mark as auto-upgrade in 1. which are present in 2.", shape="rect"]
      e [label="Install module mark as auto-install in 1. which are not present in 2.", shape="rect"]
      f [label="Remove module mark as auto-remove in 1. which are present in 2.", shape="rect"]
      g [label="Import module from 2. updated list", shape="rect"]

      a -> b -> c -> d -> e -> f -> g ;
   }

This is done by ``app.module.SmartManagement`` class.
