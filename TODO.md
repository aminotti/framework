# TODO List for v1.0 beta

## Next TODO

- Reflechir agregation de backend (filestorage dans plusieur cloud, plusieur system d'authent,...)
- Etudier possibilter de deplacer contenttype & hooks dans des modules (bases).
- Ameliorer maj structure DB qd update/upgrade/remove module
- Réfléchir à la gestion de la langue

## Documentation

- [ ] Mettre à jour la documentation
- [ ] Documenter API Rest (manager.py, hooks, ...)
- [ ] Documenter la création de plugins pour :
 * [ ] mimetype
 * [ ] hook

## Tests

### Définitions

* **TDD**
 1. Write unit test
 2. Fail the test
 3. Write code
 4. Pass the test
 5. Refactor code
* **ATDD** : *Given* <setup> *when* <trigger> *then* <verification>.
* **BDD** : TDD + BDD : http://dannorth.net/whats-in-a-story/

1. **Unit test** : Test class, method (individual piece of code).
2. **Integration test** : Test how well several units interact with each other.
3. **Acceptance test** : External view of the system. Ensure customer that the functionality meets their requirements.

* **Regression test** : re-run unit and intergration tests after all patches, upgrades, and bug fixes in order to check that no new bugs have been introduced.

### To do

curl -v -X GET -H "Accept: application/json" http://api.meezio.eu:5000/country/5/
curl -v -X GET http://api.meezio.eu:5000/binaries/country/6/photo.png

curl -v -X PUT -H "Content-Type: image/png" --data-binary @tests/flag.png http://api.meezio.eu:5000/binaries/country/5/flag.png
curl -v -X PUT -H "Content-Type: image/jpeg" --data-binary @tests/photo.jpg http://api.meezio.eu:5000/binaries/country/5/photo.jpg

/binaries/country/6/photo.png
/binaries/country/5/flag.jpg

- [x] Faire un addon 'mod_test' pour test unitaire (avec tous type de fields possible image binary fs pas fs, field minsucle, majuscule,...)
- tester country avec hookable à true
- [ ] 
- [ ] 
- [ ] 

## API REST pour gérer Yameo

- routes dans module ``app/manager.py``, appli WSGI dédiés: module ``management`` application ``manager``.
- [ ] création de module : creation de l'arbo dans répertoire addons, eventuellement tappez DB gestionnaire de projet pour genérer model YAML,... ``/modules/<module>/``
- [x] Création/suppresion de tenant : ``PUT`` & ``DELETE`` sur ``/tenants/<tenant>/`` (<tenant> = fake qd app pas multitenant)

## Création dynamique du model à partir du yaml & DB

- *Les addons ne doivent pas avoir des noms de module standards sinon ne serat pas importer.*
- [x] Héritage classic : même attribute 'name' et num 'sequence' pour priorité (Fusion avec la class mère)
- [x] Héritage par exention :  'inherit' recoit la class mère dont on veut récup les fields (Copy du dict de la class mere)
- [x] model logic (.py associé au .yalm avec utilisation API)
- [ ] Backup structure DB dans main DB pour permettre edition champs avec l'UI (TODO #200 dans context.py)
- [ ] Faire une liste de fonction standards pour les constraints (exemple lowercase, uppercase, capitalize, ...) dans un module de .app

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

- [x] _getHTTP => search() => creation d'une liste d'instance de ressource
- [x] _putHTTP => write() => creation d'un instance de la ressource (id fourni)
- [x] _postHTTP => write() => creation d'un instance de la ressource (id auto)
- [x] _patchHTTP => update() => direct update (sans creation d'instance de ressource aka on lis pas la DB avant d'ecrire)=> attention au checks
- [x] _deleteHTTP => delete() => direct delete (sans creation d'instance de ressource)
- [x] Traiter binary file
  * http://abandon.ie/notebook/simple-file-uploads-using-jquery-ajax (https://github.com/Abban/jQueryFileUpload)
  * path stockage FS : '/var/data/' + '<tenant>/<ressourcename>/<attribute>/<uuid>.<ext>
  * path URL : '/binary/' + <ressourcename>/<identifier>/<attribute>.<ext>
  * [x] Création type binaire
  * [x] POST/POST/PATCH => save data to type binaire
  * [x] save type binaire to DB et FS
  * [x] load type binaire from DB et FS (search() / get())
  * [x] Suppression type binaire : delete() (FS,  DB Ok)
  * [x] JSON convert type binaire en URL (GET ressource)
  * [x] GET d'un type binaire : '/binary/' + <ressourcename>/<identifier>/<attribute>.<ext>
  * [x] PUT/PATCH d'un type binaire : '/binary/' + <ressourcename>/<identifier>/<attribute>.<ext>

## Traiter relation interbackend

- Doc utile : https://stormpath.com/blog/linking-and-resource-expansion-rest-api-tips/

- [ ] 1-1 one2one/inherits (exemple pour user : une partie en DB, un parti en LDAP, Acces transparent au attributes)
- [ ] n-1 many2one (Ca ajoute un attribut qui contient la ressource)
- [ ] n-n many2many (Ca ajoute un attribut qui contient une liste de ressource) assoss interbackend stocker dans db principal
- [ ] Quand relation pas au sein de la meme DB ou quand backend pas DB, assoss stocké dans la DB principale de l'application.
- [ ] Traiter domain pour relation (ie: one2many pour route '/user/paris60/' [('age', '>', '60'), ('adress.city', 'like', 'Paris')])
- [ ] Création automatique des routes
- [ ] Gérer relation quand model embarqué dans meme instance (on meme document pour base NoSQL)
- [ ] Gestion des clés etrangères

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
- [x] Share key utilise alog HMAC-SHA1 : http://taigaio.github.io/taiga-doc/dist/webhooks.html#_verify_signature.

## Gestion du cache

- [x] Ajout d'un attribut boolean '_cacheable' pour dire si la ressource doit etre mise en cache ou pas
- [ ] Plusieur systeme de cache possible : redis, memchache,...

## Permission

* Auditer les requetes de Taiga pour l'authent vu que c'est full API
* Tester webservice stormpath pour voir comment sont gérer les permission avec un system d'authent détaché
* https://auth0.com/blog/2014/12/02/using-json-web-tokens-as-api-keys/
* http://jwt.io/

- [ ] RO & RW
- [ ] par fields
- [ ] par ressource (attention à respecter les droits sur les ressources liées many2many, many2one, one2one)

## Authentification

- Création d'un OpenID Provider (OP) qui :
 * faut l'authent sur une DB, un annuaire LDAP/AD, IMAP/POP, OAuth2.0,...
 * Récupere l'identité dans la DB ou dans l'annuaire LDAP/AD, ou par web service avec token OAuth.
 * Donc création de connecteurs pour les différents backend possible
- Gestion des permission : 2 possibilités :
 * Soit on utilise le 'sub' du ID token (JWS) comme identifiant et le Relying Party (RP) gère lui meme ses permissions
 * Soit l'OP permet de géré des rôles/group/scope et envoi infos dans token JWS, le RP a juste a verifier que le role requis est bien contenu dans le token. 
 * Avantage/inconvenient :
  - solution 2 permettra pas de se connecter en passant par un OP tiers 100% dynamique puisque lui ne fournira que le 'sub' dans sont token.
  - Solution 2 permet une gestion centralisé user + permission
  - Solution 2 permet de créer des role/scope/group en commun utilisable pour tout les RP
  - Solution 2 polu l'ID Token en ajoutant des infos qui ne seront pas exploiter par les RP tiers qui utiliserons notre OP
  - Solution 1 lit les role,group, permission au RP et non a l'OP => la gestion des permission en fonction des group role doit etre redeveloppez pour chaque RP.

- Web service :
 * https://stormpath.com/blog/easy-single-sign-on-idsite/
 * https://auth0.com/how-it-works
- SAML
- CAS
- https://auth0.com/docs/protocols
- https://auth0.com/docs/identityproviders

### OAuth 2.0

- https://tools.ietf.org/html/rfc6749
- https://tools.ietf.org/html/rfc6750
- https://www.digitalocean.com/community/tutorials/an-introduction-to-oauth-2
- Appli doit etre enregistré au préalable (fourni nom, url callback,...) et obtien id et password.
- 4 Types d'Authorization Grant pour obtenir le token :
 * Authorization Code: server-side Applications (app php qui va utiliser une API)
 * Implicit: Mobile Apps or HTML5/JS  App (run on the user's device)
 * Resource Owner Password Credentials: used with trusted Applications, app dev/detenu par le fournisseur d'API
 * Client Credentials: credential de l'appli, pas d'un user
- http://oauth.net/articles/authentication/#openid-connect
- http://nat.sakimura.org/2013/07/28/write-openid-connect-server-in-three-simple-steps/
- http://nat.sakimura.org/2014/12/10/making-a-javascript-openid-connect-client/
- https://auth0.com/blog/2014/01/27/ten-things-you-should-know-about-tokens-and-cookies/


## Autres

- Pour ne plus avoir a enregistrer des binary en DB modifier en ajoutant un en tete de type, faire une class qui test le type de fichier en fonction de l'empreinte du binaier (PNG dans header .png par exemple) (sinon renvoi application/octet-stream .bin)
- Refléchir à content type perso pour rendu : 
 * application/x-yameo-ui pour differrent type d'affichage ressources (label, help,...)
 * application/x-yameo-pdf (xml, xlst) pour merge template avec ressource et sort pdf...
- Rendre plugable format d'echange HTTP (json, bjson, csv,...) => voir comment on gere des rapport (PDF,)
 * http://stackoverflow.com/questions/5573215/creating-a-pdf-from-xml-using-xsl-fo-w-python
 * http://appyframework.org/podRenderingTemplates.html
- Servent Send event (action de Workflow??)
- Workflow odoo (https://www.odoo.com/documentation/8.0/reference/workflows.html) :
  * 1 Workflow est assosicé a un model
  * Composer de d'activité relié par des transition
  * 4 type d'activité : dummy, function, stop all, subworkflow
  * 3 critère pour les transition : condition, signal, trigger
- Offline, sync Online : https://auth0.com/blog/2015/10/30/creating-offline-first-web-apps-with-service-workers/
- Doc auto API rest (d'apres commentaire et codes routes???)
- UI XML to generate HTML, iOS, Android... donc code generer a partir des fichiers du backend ou separer complétement backend et frontend???.
