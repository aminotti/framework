# TODO List

## Next

- Reflechir au type binaire
 * POST/PUT/PATCH : Envoyer en mutlipart avec le binaire dans le corp
 * GET : l'attribut vaut l'URL /<ressource>/id/attribute.ext
 * l'attribut binaire n'est chargé que pour save en DB
 * pour stockage db ajouter en tete avec extension et mine_type

 * BinaryField est un dico qui cotient, mine-type, extension, data
 * mimetype et data ajouter en header du binary pour save dans db
 * les convertion vert ouput format(csv, xml,..) qui transformt le binary field en URL
 * Definir traitement qd on HTTP GET une URL d'un binary
 * Doit-on faire un traitement pour faire directemnet un PUT sur un binary?

- Faire une ressource binary/file/fsstorage dans module base pour permettre de faire facilement one2one pour save du FS au lieux DB
- créer model ORM pour save conf DB par tenant en .py (pas .yaml)
- Reflechir agregation de backend (filestorage dans plusieur cloud, plusieur system d'authent,...)
- Reflechir au cache des donnée persistance (redis, memcache) : ajouter un attribut au ressource pour dire si on veut cacher ou pas (fait: _cacheable)
- Backup structure DB dans main DB pour permettre edition champs avec l'UI (TODO #200 dans context.py)
- Ameliorer maj structure DB qd update/upgrade/remove module

## Création dynamique du model à partir du yaml

- [x] Héritage classic : même attribute 'name' et num 'sequence' pour priorité (Fusion avec la class mère)
- [x] Héritage par exention :  'inherit' recoit la class mère dont on veut récup les fields (Copy du dict de la class mere)
- [x] model logic (.py associé au .yalm avec utilisation API)
- [ ] Faire une liste de fonction standar pour les constraint (exemple lowercase, uppercase, capitalize, ...) dans un module de .app

## Implementer les fonctions de base de ORM

- [x] Methode pour splitter l'URI et setter des attributs _basedn, _rdn, _database,...)
- [x] Model.search(filter, sorted=None(field or dict of fields {'field': reverse(default False)}), count/limit=0, offset=0) : return list of matching record
- [x] Model.get(*identifiers) : renvoi une ressource
- [x] Model.delete(filter) suppression sur une liste de ressource
- [x] Model.update(fieldsname, filter) maj sur une liste de ressource
- [x] instance.create() creation d'une une ressoure
- [x] instance.write() maj d'une une ressoure
- [x] instance.unlink() suppression d'un ressource

## Implementer les http method

-  [x] _getHTTP => search() => creation d'une liste d'instance de ressource
-  [x] _putHTTP => write() => creation d'un instance de la ressource (id fourni)
-  [x] _postHTTP => write() => creation d'un instance de la ressource (id auto)
-  [x] _patchHTTP => update() => direct update (sans creation d'instance de ressource aka on lis pas la DB avant d'ecrire)=> attention au checks
-  [x] _deleteHTTP => delete() => direct delete (sans creation d'instance de ressource)
- Traiter binary file (Ajouter metadata dans header du file qd)
-  [ ] getBinary classmethod

## Traiter relation interbackend

- Doc utile : https://stormpath.com/blog/linking-and-resource-expansion-rest-api-tips/

- [ ] 1-1 one2one/inherits (exemple pour user : une partie en DB, un parti en LDAP, Acces transparent au attributes)
- [ ] n-1 many2one (Ca ajoute un attribut qui contient la ressource)
- [ ] n-n many2many (Ca ajoute un attribut qui contient une liste de ressource) assoss interbackend stocker dans db principal
- [ ] Quand relation pas au sein de la meme DB ou quand backend pas DB, assoss stocké dans la DB principale de l'application.
- [ ] Traiter domain pour relation (ie: one2many pour route '/user/paris60/' [('age', '>', '60'), ('adress.city', 'like', 'Paris')])
- [ ] Création automatique des routes

## Gestion des hooks

- [x] Pourvoir executer des hooks sur les actions write(), update(), delete(), unlink() (appel method du manager)
- [x] Creation d'une class hook manager qui va lire la DB, Charger le bon module de hook en lui envoiyant les settings deserialisé (dict)
- [x] Hook plugable : Webook pour commencer, message pour bus d'entreprise (ESB)
- [x] Chaque hook ajouter est enregistré en DB  avec les colonnes :
  * ressource (Nom de la classe en miniscule)
  * action (create, update, delete)
  * type (nom du module à utiliser : web, message)
  * date last execution
  * message d'execution
  * boolean pour activiation du hook enregistré
  * settings : parametre propre au hook (dict serialisé)
- [X] Ajouter un attribut au ressource pour definir si la ressource est hookable ou pas
- [ ] Cacher les hooks dans un redis ou memchache
- [ ] Token utiliser coté client pour calculer un hash (HMAC hexdiges) des data envoyer et calcul du meme hash coté server avec le meme token et comparaison.

## Permission

* Auditer les requetes de Taiga pour l'authent vu que c'est full API
* Tester webservice stormpath pour voir comment sont gérer les permission avec un system d'authent détaché

- [ ] RO & RW
- [ ] par fields
- [ ] par ressource (attention à respecter les droits sur les ressources liées many2many, many2one, one2one)

## Authentification

- Web service : https://stormpath.com/blog/easy-single-sign-on-idsite/

## Autres

- Rendre plugable format d'echange HTTP (json, bjson, csv,...) => voir comment on gere des rapport (PDF,)
- Servent Send event (action de Workflow??)
- Workflow odoo (https://www.odoo.com/documentation/8.0/reference/workflows.html) :
  * 1 Workflow est assosicé a un model
  * Composer de d'activité relié par des transition
  * 4 type d'activité : dummy, function, stop all, subworkflow
  * 3 critère pour les transition : condition, signal, trigger
- Offline, sync Online
- Doc auto API rest (d'apres commentaire et codes routes???)
- UI XML to generate HTML, iOS, Android... donc code generer a partir des fichiers du backend ou separer complétement backend et frontend???.
