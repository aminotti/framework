./app/module.py:113:        # TODO implementer install module avec ajout de route
./app/module.py:125:        # TODO ajout de route
./app/module.py:134:        # TODO implementer remove module avec ajout de route
./app/module.py:156:        # TODO remplacer tout le bloc pas chargement depuis DB des module deja installé pour ce tenant
./app/module.py:168:            # TODO gerer install des dependances python qd elle sont pas présente
./app/module.py:169:            # TODO gerer dependance d'autre module => on ajout tous les modules dont il depend (doit etre recursif) à cls.installed
./app/module.py:177:            # TODO import DATA
./app/module.py:182:            # TODO call onRemove() from all module's model
./app/module.py:183:            # TODO gerer dependance d'autre module => on supprime tous les modules qui depende de lui (doit etre recursif)
./app/module.py:188:        # TODO save installed to DB
./app/module.py:220:        # TODO Import view (xml) for current tenant/app
./app/module.py:221:        # TODO Import data (json, yaml, csv) for current tenant/app
./app/module.py:222:        # TODO Import workflow (xml ? yaml?) for current tenant/app
./app/module.py:226:        # TODO si docker avec plusieurs instance de lancé, killer les autres instances
./app/module.py:227:        # TODO Remove views
./app/module.py:228:        # TODO Remove datas
./app/module.py:229:        # TODO Remove workflows
./app/api.py:45:            # Run method if one of the TODO ameliorer commentaire
./app/multitenancy.py:110:            # TODO Creation auto de db (et des different backend pour ce tenancy) et populate si un param de conf est a true pour auto create tenancy et ajout d'une route special pour faire ca.
./lib/httpmethod.py:34:    # TODO gerer different input et ouput de facon modulaire (csv, json, bjson...)
./lib/httpmethod.py:35:    # TODO Gerer les accept et content type header
./lib/httpmethod.py:101:        r = Response(obj2json(data), headers=cls.__headers)  # TODO change convert method according to client 'Accept' header
./lib/httpmethod.py:173:            pass  # TODO implementaire pour binary
./lib/httpmethod.py:190:            # TODO Handle multipart/mixed
./lib/context.py:80:        # TODO checker champs requis présent dans yaml et bon type associé
./lib/context.py:87:                # TODO #200 cls._regiteredModels[tenant][key].append(<data from DB for this model/ressource>)
Fichier binaire ./lib/orm/pool.pyc correspondant
./lib/orm/pool.py:33:.. todo::
./lib/orm/fields.py:187:        # TODO implémenter la conversion à la bonne taille
./lib/orm/mysql/orm.py:56:        # TODO Eventuellement parser les params (infos[5]) pour recup db options (genre charset, autocommit,...)
./lib/orm/mysql/orm.py:65:        # TODO create table if not exist
./lib/orm/mysql/orm.py:66:        # TODO exec add columns ALTER TABLE `users` ADD `date` DATE NULL DEFAULT NULL ;
./lib/orm/mysql/orm.py:67:        # TODO si failure exec modify columns ALTER TABLE `users` MODIFY `date` DATE NULL DEFAULT NULL ;
./lib/orm/mysql/sql.py:139:        # TODO gerer creation foreign key
./lib/orm/mysql/sql.py:277:        # TODO gerer binary field pour create columns
./lib/orm/base.py:62:                # TODO gerer relations
./lib/orm/base.py:75:    # TODO Add internal fields (on backend herited class??)
./lib/orm/base.py:130:            # TODO Check ACL RW allowed
./lib/orm/base.py:133:            # TODO trigger workflow event onchange
./lib/orm/base.py:153:        # TODO elif name in self._one2one._columns: (boucler sur self._one2one pour avoir acces aux ._columns)
./lib/orm/base.py:160:            # TODO Check ACL RO or RW allowed
./lib/orm/base.py:170:        # TODO elif name in self._one2one._columns: (boucler sur self._one2one pour avoir acces aux ._columns)
./lib/orm/base.py:238:        # TODO implement en retirant les champs mis a copy=False
./TODO_List.md:1:./app/module.py:113:        # TODO implementer install module avec ajout de route
./TODO_List.md:2:./app/module.py:125:        # TODO ajout de route
./TODO_List.md:3:./app/module.py:134:        # TODO implementer remove module avec ajout de route
./TODO_List.md:4:./app/module.py:156:        # TODO remplacer tout le bloc pas chargement depuis DB des module deja installé pour ce tenant
./TODO_List.md:5:./app/module.py:168:            # TODO gerer install des dependances python qd elle sont pas présente
./TODO_List.md:6:./app/module.py:169:            # TODO gerer dependance d'autre module => on ajout tous les modules dont il depend (doit etre recursif) à cls.installed
./TODO_List.md:7:./app/module.py:177:            # TODO import DATA
./TODO_List.md:8:./app/module.py:182:            # TODO call onRemove() from all module's model
./TODO_List.md:9:./app/module.py:183:            # TODO gerer dependance d'autre module => on supprime tous les modules qui depende de lui (doit etre recursif)
./TODO_List.md:10:./app/module.py:188:        # TODO save installed to DB
./TODO_List.md:11:./app/module.py:220:        # TODO Import view (xml) for current tenant/app
./TODO_List.md:12:./app/module.py:221:        # TODO Import data (json, yaml, csv) for current tenant/app
./TODO_List.md:13:./app/module.py:222:        # TODO Import workflow (xml ? yaml?) for current tenant/app
./TODO_List.md:14:./app/module.py:226:        # TODO si docker avec plusieurs instance de lancé, killer les autres instances
./TODO_List.md:15:./app/module.py:227:        # TODO Remove views
./TODO_List.md:16:./app/module.py:228:        # TODO Remove datas
./TODO_List.md:17:./app/module.py:229:        # TODO Remove workflows
./TODO_List.md:18:./app/api.py:45:            # Run method if one of the TODO ameliorer commentaire
./TODO_List.md:19:./app/multitenancy.py:110:            # TODO Creation auto de db (et des different backend pour ce tenancy) et populate si un param de conf est a true pour auto create tenancy et ajout d'une route special pour faire ca.
./TODO_List.md:20:./lib/httpmethod.py:34:    # TODO gerer different input et ouput de facon modulaire (csv, json, bjson...)
./TODO_List.md:21:./lib/httpmethod.py:35:    # TODO Gerer les accept et content type header
./TODO_List.md:22:./lib/httpmethod.py:101:        r = Response(obj2json(data), headers=cls.__headers)  # TODO change convert method according to client 'Accept' header
./TODO_List.md:23:./lib/httpmethod.py:173:            pass  # TODO implementaire pour binary
./TODO_List.md:24:./lib/httpmethod.py:190:            # TODO Handle multipart/mixed
./TODO_List.md:25:./lib/context.py:80:        # TODO checker champs requis présent dans yaml et bon type associé
./TODO_List.md:26:./lib/context.py:87:                # TODO #200 cls._regiteredModels[tenant][key].append(<data from DB for this model/ressource>)
./TODO_List.md:28:./lib/orm/pool.py:33:.. todo::
./TODO_List.md:29:./lib/orm/fields.py:187:        # TODO implémenter la conversion à la bonne taille
./TODO_List.md:30:./lib/orm/mysql/orm.py:56:        # TODO Eventuellement parser les params (infos[5]) pour recup db options (genre charset, autocommit,...)
./TODO_List.md:31:./lib/orm/mysql/orm.py:65:        # TODO create table if not exist
./TODO_List.md:32:./lib/orm/mysql/orm.py:66:        # TODO exec add columns ALTER TABLE `users` ADD `date` DATE NULL DEFAULT NULL ;
./TODO_List.md:33:./lib/orm/mysql/orm.py:67:        # TODO si failure exec modify columns ALTER TABLE `users` MODIFY `date` DATE NULL DEFAULT NULL ;
./TODO_List.md:34:./lib/orm/mysql/sql.py:139:        # TODO gerer creation foreign key
./TODO_List.md:35:./lib/orm/mysql/sql.py:277:        # TODO gerer binary field pour create columns
./TODO_List.md:36:./lib/orm/base.py:62:                # TODO gerer relations
./TODO_List.md:37:./lib/orm/base.py:75:    # TODO Add internal fields (on backend herited class??)
./TODO_List.md:38:./lib/orm/base.py:130:            # TODO Check ACL RW allowed
./TODO_List.md:39:./lib/orm/base.py:133:            # TODO trigger workflow event onchange
./TODO_List.md:40:./lib/orm/base.py:153:        # TODO elif name in self._one2one._columns: (boucler sur self._one2one pour avoir acces aux ._columns)
./TODO_List.md:41:./lib/orm/base.py:160:            # TODO Check ACL RO or RW allowed
./TODO_List.md:42:./lib/orm/base.py:170:        # TODO elif name in self._one2one._columns: (boucler sur self._one2one pour avoir acces aux ._columns)
./TODO_List.md:43:./lib/orm/base.py:238:        # TODO implement en retirant les champs mis a copy=False
