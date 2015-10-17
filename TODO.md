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
./lib/httpmethod.py:39:    # TODO gerer different input et ouput (csv, json,...)
./lib/httpmethod.py:128:        r = Response(obj2json(data), headers=cls.__headers)  # TODO change convert method according to client 'Accept' header
./lib/httpmethod.py:143:            url = request.base_url + '/' + str(rowid)  # TODO check que l'URL est bonne
./lib/httpmethod.py:175:        # dico = cls.getDataFromContentType() TODO
./lib/httpmethod.py:217:            # TODO Handle multipart/mixed
./lib/context.py:78:        # TODO checker champs requis présent dans yaml et bon type associé
Fichier binaire ./lib/orm/pool.pyc correspondant
./lib/orm/pool.py:33:.. todo::
./lib/orm/fields.py:189:        # TODO implémenter la conversion à la bonne taille
./lib/orm/mysql/orm.py:56:        # TODO Eventuellement parser les params (infos[5]) pour recup db options (genre charset, autocommit,...)
./lib/orm/mysql/orm.py:65:        # TODO create table if not exist
./lib/orm/mysql/orm.py:66:        # TODO exec add columns ALTER TABLE `users` ADD `date` DATE NULL DEFAULT NULL ;
./lib/orm/mysql/orm.py:67:        # TODO si failure exec modify columns ALTER TABLE `users` MODIFY `date` DATE NULL DEFAULT NULL ;
./lib/orm/mysql/sql.py:189:        # TODO gerer binary field pour create columns
./lib/orm/base.py:62:                # TODO gerer relations
./lib/orm/base.py:75:    # TODO Add internal fields (on backend herited class??)
./lib/orm/base.py:130:            # TODO Check ACL RW allowed
./lib/orm/base.py:133:            # TODO trigger workflow event onchange
./lib/orm/base.py:159:            # TODO Check ACL RO or RW allowed
./lib/orm/base.py:213:        # TODO implement en retirant les champs mis a copy=False
./lib/orm/base.py:266:        # TODO renvoyer l'id pour une creation!!
