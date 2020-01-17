#### Required:
* [x] Remove API_TOKEN from GET variable
* [x] when TOKEN_API is not correct, return 401 not 404 #31
* [ ] fix the old way to update tile
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
* [ ] Add Contrib.md
* [x] Test it on windows
* [ ] Propose real docker img with/without redis
* [ ] publish a public tipboard to show build CI/CD stats of project
* [ ] made issue #32 possible
* [ ] Update the user doc for /update
* [x] Fix Badge status in Readme.md
* [ ] Write script to put in production ready mode (minify JS, debug=False, etc)


---->
Tu test la meta des text tiles mais il y a deux méthode /tileconfig/XXX & /update
et tu na jamais test la /update
donc il faut dabord test que /tileconfig work


- Les meta des chart TEXT ne sont pas update par sonde
- pie_chart est basé sur l'ancienne sonde et casse le principe d'update à cause du pie_data_value
- v2Regression tofix: pie, radar, cumul, line, norm
- Le mode production ne prends pas en compte les /static
- palette.js doit etre cassé pour etre un objet dans tipboard.js
- la sonde Listing est a fix
- les erreurs (ex:tile_template not found), ne sont plus affiché dans le dashboard
- Flip time parsé depuis le .yaml si présent
-
-


#### Optional

* add color blind mode :)
* Deploy to Azure
* Eazy way to secure dashboard with authentification view
* Add matomo iframe widget as tile :D
* Propose an interactive/GUI way to build your custom_layout !


If we do that, we can go to sleep ez


##### NB To update Documentation
