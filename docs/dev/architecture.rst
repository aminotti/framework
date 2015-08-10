Architecture
============


.. graphviz::

   graph test {
      splines=ortho
      edge [dir=both,arrowhead=vee,arrowtail=vee];

      LDAP [shape=Mcircle,gradientangle=90,fillcolor="#EF734E:#FFFBFA",width=1,fixedsize=true];
      MySQL [shape=Mcircle,gradientangle=90,style="filled",fillcolor="#03BB5E:#F7FDFA",width=1,fixedsize=true];
      PosgreSQL [shape=Mcircle,gradientangle=90,style="filled",fillcolor="#03BB5E:#F7FDFA",width=1.2,fixedsize=true];
      SQLite [shape=Mcircle,gradientangle=90,style="filled",fillcolor="#03BB5E:#F7FDFA",width=1,fixedsize=true];
      Models [shape=rec,width=4,fixedsize=true,gradientangle=90,style="filled",fillcolor="#E0E6EC:#ADCFFF"];
      web [shape=rec,width=4,fixedsize=true,label="Web service";gradientangle=90,style="filled",fillcolor="#E0E6EC:#ADCFFF"];

      LDAP -- Models;
      MySQL -- Models;
      PosgreSQL -- Models;
      SQLite -- Models;
      Models -- web [style=invis,len=2];
   }
