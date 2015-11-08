# TODO LIST

|File|Ligne|todo|
|----|-----|----|
|app/module.py|113| implementer install module avec ajout de route|
|app/module.py|125| ajout de route|
|app/module.py|134| implementer remove module avec ajout de route|
|app/module.py|156| remplacer tout le bloc pas chargement depuis DB des module deja installé pour ce tenant|
|app/module.py|168| gerer install des dependances python qd elle sont pas présente|
|app/module.py|169| gerer dependance d'autre module => on ajout tous les modules dont il depend (doit etre recursif) à cls.installed|
|app/module.py|177| import DATA|
|app/module.py|182| call onRemove() from all module's model|
|app/module.py|183| gerer dependance d'autre module => on supprime tous les modules qui depende de lui (doit etre recursif)|
|app/module.py|188| save installed to DB|
|app/module.py|220| Import view (xml) for current tenant/app|
|app/module.py|221| Import data (json, yaml, csv) for current tenant/app|
|app/module.py|222| Import workflow (xml ? yaml?) for current tenant/app|
|app/module.py|226| si docker avec plusieurs instance de lancé, killer les autres instances|
|app/module.py|227| Remove views|
|app/module.py|228| Remove datas|
|app/module.py|229| Remove workflows|
|app/module.py|235| reimporter defaults routes|
|app/api.py|45|Run method if one of the  ameliorer commentaire|
|app/multitenancy.py|113| Creation auto de db (et des different backend pour ce tenancy) et populate si un param de conf est a true pour auto create tenancy et ajout d'une route special pour faire ca.|
|lib/httpmethod.py|54| add expend = True pour toucher les relation au lieux de leur id|
|lib/httpmethod.py|55| ajouter un attribute expend = request.args.get('expend', False) pour geré si renvoi url des relations ou data completes|
|lib/httpmethod.py|103| Set ressource language : request 'Accept-Language' and set reponse 'Content-Language'|
|lib/httpmethod.py|191| RFC2616 sect 14.1, si wrong 'Accept' header : 406 (Not Acceptable). Si * ou pas de 'Accept' alors default json|
|lib/httpmethod.py|223| documenter les different content-type possible avec leur contenu de body|
|lib/httpmethod.py|229| gerer POST normal (x-www-form-urlencode) formulaire (voir tests/form.html)|
|lib/httpmethod.py|234| Actuelement un seul attribut de form envoyer qui contient un json avec tout les fields :|
|lib/httpmethod.py|249| Handle multipart/mixed, faire une lib pour gere corp http/mail :|
|lib/context.py|80| checker champs requis présent dans yaml et bon type associé|
|lib/context.py|87|200 cls._regiteredModels[tenant][key].append(<data from DB for this model/ressource>)|
|lib/orm/binary.py|55| get relative URL|
Fichier binaire ./lib/orm/pool.pyc correspondant|
|lib/orm/pool.py|33:.. todo::|
|lib/orm/fields.py|189| implémenter la conversion à la bonne taille|
Fichier binaire ./lib/orm/mysql/sql.pyc correspondant|
|lib/orm/mysql/orm.py|56| Eventuellement parser les params (infos[5]) pour recup db options (genre charset, autocommit,...)|
|lib/orm/mysql/orm.py|65| create table if not exist|
|lib/orm/mysql/orm.py|66| exec add columns ALTER TABLE `users` ADD `date` DATE NULL DEFAULT NULL ;|
|lib/orm/mysql/orm.py|67| si failure exec modify columns ALTER TABLE `users` MODIFY `date` DATE NULL DEFAULT NULL ;|
|lib/orm/mysql/sql.py|98| remove compute field from CREATE TABLE (resu of cls.__getColumnsSQL())|
|lib/orm/mysql/sql.py|126:         Remplace l'attribut contenant les métadonnées d'un binary par une URL.|
|lib/orm/mysql/sql.py|142| Change metadata par URL quand type BinaryCol|
|lib/orm/mysql/sql.py|211| gerer creation foreign key|
|lib/orm/base.py|64| gerer relations|
|lib/orm/base.py|83| Add internal fields (on backend herited class??)|
|lib/orm/base.py|138| Check ACL RW allowed|
|lib/orm/base.py|146| trigger workflow event onchange|
|lib/orm/base.py|166| elif name in self._one2one._columns: (boucler sur self._one2one pour avoir acces aux ._columns)|
|lib/orm/base.py|173| Check ACL RO or RW allowed|
|lib/orm/base.py|183| elif name in self._one2one._columns: (boucler sur self._one2one pour avoir acces aux ._columns)|
|lib/orm/base.py|251| implement en retirant les champs mis a copy=False|
|lib/orm/base.py|272| add expend = True pour toucher les relation au lieux de leur id|
