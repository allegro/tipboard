- TOFIX:
    - cache.get fais un doublon sur la sérialization str -> Json ce qui nest pas le cas dans cache.redis.get
    - update les meta: il y a une incompréhension si je dois send config.options ou options sur les différentes chart
    - vbar is not recognize in template

- CI
    - si on pouvait également une bonne fois pour toute enlever les lib test des dependencies

- chartJS:
    - tu add la linear gauge chart, depuis une update chelou de ChartJS sur github
    - https://github.com/scottmcculloch/Chart.LinearGauge.js/blob/master/index.html
    - dans l'index il y a plein d'exemple de gauge utilisé, comprends et reprends le mécanisme
    - tu as add trois fonction directement dans testèlinearradial.js
        - chart.element.gaugerect.js
        - chart.lineargauge.js
        - chart.scale.lineargauge.js
    tu as add tout ce qu'il faut pour l'ajouter mais il faudrait play le index.html
    pour voir les différents types qui existe et en choisir 1 ou plusieur à implémenter dans tipboard


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
