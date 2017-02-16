# Development Notes

New project created via:

* `mkproject -p /usr/local/bin/python3 quod`
* `ln -s ~/.virtualenvs/quod/lib ./lib`
* `ln -s ~/.virtualenvs/quod/bin ./bin`
*  Created new repo on GitHub
*  `git clone git@github.com:ouh-churchill/quod.git quod_repo`
*  `cd quod_repo/`
*  `mkdir requirements`
*  `touch requirements/common.txt`
*  `touch requirements/development.txt`
*  Open the project in PyCharm.
*  Edit the two requirements files
*  `pip install -r requirements/development.txt `
*  `mkdir docs`
*  Generate this development.md file
*  `wagtail start quodsite`
*  `cd quodsite`
*  `python manage.py migrate` (nb: local alias of `pm` for `python manage.py` used hereon
*  `pm createsuperuser` Using mostly defaults for test purposes

Then begin playing with the setup...

Useful links

* http://docs.wagtail.io/en/latest/getting_started/tutorial.html
* https://github.com/springload/awesome-wagtail
* https://github.com/rkhleics/wagtailmenus
* http://quod.org.uk