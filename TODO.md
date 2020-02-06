Documenter ce qu'on met dans le .json et ce qu'on met dans les yaml et comment on s'en sert
    - Comment changer les couleurs
    - Comment faire tourner une tile
    - La rotation des dashboard
    - Definir les différent Docker

- TOFIX:
    - cache.get fais un doublon sur la sérialization str -> Json
    - ce qui nest pas le cas dans cache.redis.get

- iframe
    - Bug Rework JS
        - on dirait que lorsque tu load un autre dashboard si tu nas pas les .js & .css, tu na pas bootstrap
        - comme si a chaque load de nouveau dash, il faut load de nouveau les .js & .css bootstrap etc
        - pourtant dans flipboard.js, tu ne change(en js) que le body, donc le head, avec les devrait etre actif
    - quand tu look direct un dashboard (non flipboard), les js ne sont plus du tout ajouter
        - il faut réussir a savoir si on bient de / ou de /dashboard, car / import 1 fois all .js
        - mais si on va dans /dashboard, il faut quand meme reussir à les import

- IFRAME IS DEAD LONG LIVE TO AJAX
    - il faut réparer les import .js (activation websock & donc tile update uniquement post ajax ok dans Flipboard.js)

    - CEST UNE IFRAME DONC ON RETOURNE UNE PAGE HTML COMPLETE DONC AVEC DAUTRE D2PENDENCE
    - Il faut renvoyé de l'html <div> au lieu d'une trame HTTP
    - faire l'update de la div avec un fadeIn au lieu de replace l'iframe par une nouvelle

- MODE BLACK&WHITE
    - var:
        - body 212121 -> FFFFF
        - layout.html card shadow -> card
        - background-color: #313131 -> #f5f5f5;
        - Js tipboard.initChartjsDefault: Chart.defaults.global.defaultFontColor = "rgba(255, 255, 255, 0.83)"; -> black
        - Js ChartJs Chart.defaults.scale.gridLines.color = "#929292";
        - ChartJs il faudra surement un peu moins de black sur les gridlines
        - css .h2 .h3 .h6 FFFFF -> 212121
        - css .tile > .tile-header rgba(255,255,255,0.1) -> black
        - switch tipboard logo
        - Txt tile:
            - Bigvalue ctr+A -white -> nothing
            - Simpleper ctr+A -white -> nothing
            - Text span -white -> nothing
           - trouver la bonne valeur text noir pour les h3
        - tu as transformer tout les #696969 et #414141  en #525252, car ca rend mieux en white
            - a voir si ca marche avec le black mode


- Finir les unitest:
    - Informer cache.py que c'est un test, pour taper sur -n 5, qu'il supprime à la fin de RUN (comme lepurge BDD)
    - Par docker les test dans gitlab-ci été casssé, car dans les test il créé une fake bdd
    - mais navait pas les droits pour tester les tiles text en testant un scénario Sondes -> parse result in html
    - for PRODUCTION MODE, if cat -R * | grep "# no pragma" == Sucess => FAILED
    - Corriger les C.I, nottament pour leur ajouter redis

* [ ] Propose real docker with gitlab-ci
    -
img with/without redis

- Django Swagger:
    - ajout de 'swagger_render'
    - ajout d'une docs/index.yml defaut a remplacer par un vrai
    - il ne trouve pas le fichier index.yml

- Le mode production ne prends pas en compte les /static
    - Créer runner de mise en prod:
        - rassemble all js to 1 file + minify it
        - DEBUG = True -> False
        - charger les static sur un CDN public


#### Required:
* [x] Remove API_TOKEN from GET variable
* [x] when TOKEN_API is not correct, return 401 not 404 #31
* [x] fix the fadding possibility
* [x] publish sensors exemple

* [ ] CD AWS
* [ ] CD Openshift
* [ ] Made a dev Wiki
* [ ] Make a real wiki to deploy in clouds
* [x] Animation when tile update
* [x] Make compatible with Python 3.4 & 3.5 & 3.6
* [x] Grid layout with flex
* [x] Let's material design the tiles ! (Its 2019 ffs)
* [x] Test it on windows
* [ ] made issue #32 possible
* [x] Fix Badge status in Readme.md
* [ ] Write script to put in production ready mode (minify JS, debug=False, etc)


---->

#### Optional

* [ ] publish a public tipboard to show build CI/CD stats of project
* Eazy way to secure dashboard with authentification view
* Add matomo iframe widget as tile :D
* Propose an interactive/GUI way to build your custom_layout !


If we do that, we can go to sleep ez


##### NB To update Documentation
