

- TOFIX:
    - cache.get fais un doublon sur la sérialization str -> Json
    - ce qui nest pas le cas dans cache.redis.get
    - update les meta: il y a une incompréhension si je dois send config.options ou options sur les différentes chart
    - DANS tipboard.jsinitTipboardObject.chartsIds vs Tipboard.chartJsTile what the difference ?



- MODE BLACK&WHITE
    - var:
        - [css] body 212121 -> FFFFF
        - [css] .h2 .h3 .h6 FFFFF -> 212121
        - [css] .tile > .tile-header rgba(255,255,255,0.1) -> black
        - [css] background-color: #313131 -> #f5f5f5;
        - [js] Js tipboard.initChartjsDefault: Chart.defaults.global.defaultFontColor = "rgba(255, 255, 255, 0.83)"; -> black
        - [js] Js ChartJs Chart.defaults.scale.gridLines.color = "#929292";
        - [python-template] layout.html card shadow -> card
        - [python-fakeData] ChartJs il faudra surement un peu moins de black sur les gridlines
        - [python-template] switch tipboard logo
        - [python-template] Txt tile:
            - Bigvalue ctr+A -white -> nothing
            - Simpleper ctr+A -white -> nothing
            - Text span -white -> nothing
           - trouver la bonne valeur text noir pour les h3
        - [css/python-template] tu as transformer tout les #696969 et #414141  en #525252, car ca rend mieux en white
            - a voir si ca marche avec le black mode

- Console mode debug et production to show Js log deep

- Finir les unitest:
    - Informer cache.py que c'est un test, pour taper sur -n 5, qu'il supprime à la fin de RUN (comme lepurge BDD)
    - Par docker les test dans gitlab-ci été casssé, car dans les test il créé une fake bdd
    - mais navait pas les droits pour tester les tiles text en testant un scénario Sondes -> parse result in html
    - for PRODUCTION MODE, if cat -R * | grep "# no pragma" == Sucess => FAILED
    - Corriger les C.I, nottament pour leur ajouter redis

* [ ] made issue #32 possible

#### Optional

* [ ] publish a public tipboard to show build CI/CD stats of project
* Eazy way to secure dashboard with authentification view
* Add matomo iframe widget as tile :D
* Propose an interactive/GUI way to build your custom_layout !

If we do that, we can go to sleep ez

* [ ] Propose real docker with gitlab-ci
    - img with/without redis

- Le mode production ne prends pas en compte les /static
    - Créer runner de mise en prod:
        - rassemble all js to 1 file + minify it
        - DEBUG = True -> False
        - charger les static sur un CDN public
##### NB To update Documentation
Documenter ce qu'on met dans le .json et ce qu'on met dans les yaml et comment on s'en sert
    - Comment changer les couleurs
    - Comment faire tourner une tile
    - La rotation des dashboard
    - Definir les différent Docker


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

* [x] Fix Badge status in Readme.md
* [ ] Write script to put in production ready mode (minify JS, debug=False, etc)
