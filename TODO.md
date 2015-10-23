# TODO List

## Next

- Reflechir au type binaire
- créer model ORM pour save conf DB par tenant en .py (pas .yaml)
- Backup structure DB dans main DB pour permettre edition champs avec l'UI (TODO #200 dans context.py)
- Ameliorer maj structure DB qd update/upgrade/remove module
- Gerer des routes dans un module python appart (Create DB, install module ...)


## Création dynamique du model à partir du yaml

- [x] Héritage classic : même attribute 'name' et num 'sequence' pour priorité (Fusion avec la class mère)
- [x] Héritage par exention :  'inherit' recoit la class mère dont on veut récup les fields (Copy du dict de la class mere)
- [x] model logic (.py associé au .yalm avec utilisation API)

## Implementer les fonctions de base de ORM

- [x] Methode pour splitter l'URI et setter des attributs _basedn, _rdn, _database,...)
- Classmethod (sur les liste de ressource)
 - [x] Model.search(filter, sorted=None(field or dict of fields {'field': reverse(default False)}), count/limit=0, offset=0) : return list of matching record
 - [x] Model.delete(filter)
- Instance method (sur une ressource)
 - [x] instance.update(fieldsname, filter)
 - [x] instance.write()
 - [x] instance.unlink()

## Implementer les http method

-  [x] _getHTTP => search() => creation d'une liste d'instance de ressource
-  [x] _putHTTP => write() => creation d'un instance de la ressource
-  [x] _postHTTP => write() => creation d'un instance de la ressource
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

## Permission

Tester webservice stormpath pour voir comment sont gérer les permission avec un system d'authent détaché

- [ ] RO & RW
- [ ] par fields
- [ ] par ressource (attention à respecter les droits sur les ressources liées many2many, many2one, one2one)

## Authentification

- Web service : https://stormpath.com/blog/easy-single-sign-on-idsite/

## Autres

- Rendre plugable format d'echange HTTP (json, bjson, csv,...) => voir comment on gere des rapport (PDF,)
- Servent Send event (action de Workflow??)
- Workflow
- Offline, sync Online
- Doc auto API rest (d'apres commentaire et codes routes???)
- UI XML to generate HTML, iOS, Android... donc code generer a partir des fichiers du backend ou separer complétement backend et frontend???.
