# TODO LIST

|File|Ligne|todo|
|----|-----|----|
|app/module.py|111| implementer install module avec ajout de route|
|app/module.py|123| ajout de route|
|app/module.py|132| implementer remove module avec ajout de route|
|app/module.py|159| gerer install des dependances python qd elle sont pas présente|
|app/module.py|160| gerer dependance d'autre module => on ajout tous les modules dont il depend (doit etre recursif) à cls.installed|
|app/module.py|172| import DATA|
|app/module.py|177| call onRemove() from all module's model|
|app/module.py|178| gerer dependance d'autre module => on supprime tous les modules qui depende de lui (doit etre recursif)|
|app/module.py|213| Import view (xml) for current tenant/app|
|app/module.py|214| Import data (json, yaml, csv) for current tenant/app (version prod: ex nomeclature & version demo: ex echantillons de données)|
|app/module.py|215| Import workflow (xml ? yaml?) for current tenant/app|
|app/module.py|219| si docker avec plusieurs instance de lancé, killer les autres instances|
|app/module.py|220| Remove views|
|app/module.py|221| Remove datas|
|app/module.py|222| Remove workflows|
|app/module.py|228| reimporter defaults routes|
|app/api.py|45|Run method if one of the  ameliorer commentaire|
|app/defaults_routes.py|39| gerer les permissions sur toutes les routes|
|lib/httpmethod.py|54| add expend = True pour toucher les relation au lieux de leur id|
|lib/httpmethod.py|55| ajouter un attribute expend = request.args.get('expend', False) pour geré si renvoi url des relations ou data completes|
|lib/httpmethod.py|103| Set ressource language : request 'Accept-Language' and set reponse 'Content-Language'|
|lib/httpmethod.py|192| RFC2616 sect 14.1, si wrong 'Accept' header : 406 (Not Acceptable). Si * ou pas de 'Accept' alors default json|
|lib/httpmethod.py|224| documenter les different content-type possible avec leur contenu de body|
|lib/httpmethod.py|230| gerer POST normal (x-www-form-urlencode) formulaire (voir tests/form.html)|
|lib/httpmethod.py|235| Actuelement un seul attribut de form envoyer qui contient un json avec tout les fields :|
|lib/httpmethod.py|250| Handle multipart/mixed, faire une lib pour gere corp http/mail :|
|lib/context.py|80| checker champs requis présent dans yaml et bon type associé|
|lib/context.py|87|200 cls._regiteredModels[tenant][key].append(<data from DB for this model/ressource>)|
Fichier binaire ./lib/orm/pool.pyc correspondant|
|lib/orm/pool.py|33:.. todo::|
|lib/orm/fields.py|191| implémenter la conversion à la bonne taille|
|lib/orm/mysql/orm.py|57| Eventuellement parser les params (infos[5]) pour recup db options (genre charset, autocommit,...)|
|lib/orm/mysql/orm.py|58| Gerer charset mysql parametrable dans uri 'utf8mb4'|
|lib/orm/mysql/orm.py|75| create table if not exist|
|lib/orm/mysql/orm.py|76| exec add columns ALTER TABLE `users` ADD `date` DATE NULL DEFAULT NULL ;|
|lib/orm/mysql/orm.py|77| si failure exec modify columns ALTER TABLE `users` MODIFY `date` DATE NULL DEFAULT NULL ;|
|lib/orm/mysql/orm.py|102| A chaque modification, un nouveau fichier est créer sur le FS par BinearyField avec backendFS|
|lib/orm/mysql/sql.py|108| remove compute field from CREATE TABLE (resu of cls.__getColumnsSQL())|
|lib/orm/mysql/sql.py|248| gerer creation foreign key|
|lib/orm/base.py|65| gerer relations|
|lib/orm/base.py|86| Add internal fields (on backend herited class??)|
|lib/orm/base.py|141| Check ACL RW allowed|
|lib/orm/base.py|150| trigger workflow event onchange|
|lib/orm/base.py|175| elif name in self._one2one._columns: (boucler sur self._one2one pour avoir acces aux ._columns)|
|lib/orm/base.py|182| Check ACL RO or RW allowed|
|lib/orm/base.py|192| elif name in self._one2one._columns: (boucler sur self._one2one pour avoir acces aux ._columns)|
|lib/orm/base.py|260| implement en retirant les champs mis a copy=False|
|lib/orm/base.py|281| add expend = True pour toucher les relation au lieux de leur id|
