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
./lib/httpmethod.py:52:        # TODO add expend = True pour toucher les relation au lieux de leur id
./lib/httpmethod.py:53:        # TODO ajouter un attribute expend = request.args.get('expend', False) pour geré si renvoi url des relations ou data completes
./lib/httpmethod.py:101:        # TODO Set ressource language : request 'Accept-Language' and set reponse 'Content-Language'
./lib/httpmethod.py:218:            pass  # TODO implementaire pour binary
./lib/httpmethod.py:235:            # TODO Handle multipart/mixed
./lib/context.py:80:        # TODO checker champs requis présent dans yaml et bon type associé
./lib/context.py:87:                # TODO #200 cls._regiteredModels[tenant][key].append(<data from DB for this model/ressource>)
Fichier binaire ./lib/orm/pool.pyc correspondant
./lib/orm/pool.py:33:.. todo::
./lib/orm/fields.py:187:        # TODO implémenter la conversion à la bonne taille
Fichier binaire ./lib/orm/mysql/sql.pyc correspondant
./lib/orm/mysql/orm.py:56:        # TODO Eventuellement parser les params (infos[5]) pour recup db options (genre charset, autocommit,...)
./lib/orm/mysql/orm.py:65:        # TODO create table if not exist
./lib/orm/mysql/orm.py:66:        # TODO exec add columns ALTER TABLE `users` ADD `date` DATE NULL DEFAULT NULL ;
./lib/orm/mysql/orm.py:67:        # TODO si failure exec modify columns ALTER TABLE `users` MODIFY `date` DATE NULL DEFAULT NULL ;
./lib/orm/mysql/sql.py:95:        # TODO remove compute field from CREATE TABLE (resu of cls.__getColumnsSQL())
./lib/orm/mysql/sql.py:123:        TODO Remplace l'attribut contenant les métadonnées d'un binary par une URL.
./lib/orm/mysql/sql.py:137:            # TODO Change metadata par URL quand type BinaryCol
./lib/orm/mysql/sql.py:206:        # TODO gerer creation foreign key
./lib/orm/mysql/sql.py:344:        # TODO gerer binary field pour create columns
./lib/orm/base.py:62:                # TODO gerer relations
./lib/orm/base.py:75:    # TODO Add internal fields (on backend herited class??)
./lib/orm/base.py:130:            # TODO Check ACL RW allowed
./lib/orm/base.py:133:            # TODO trigger workflow event onchange
./lib/orm/base.py:153:        # TODO elif name in self._one2one._columns: (boucler sur self._one2one pour avoir acces aux ._columns)
./lib/orm/base.py:160:            # TODO Check ACL RO or RW allowed
./lib/orm/base.py:170:        # TODO elif name in self._one2one._columns: (boucler sur self._one2one pour avoir acces aux ._columns)
./lib/orm/base.py:238:        # TODO implement en retirant les champs mis a copy=False
./lib/orm/base.py:259:    def get(cls, *identifiers):  # TODO add expend = True pour toucher les relation au lieux de leur id
