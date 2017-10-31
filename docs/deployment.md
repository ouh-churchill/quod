# Deployment

Dev.NDS is (being) setup to to hold multiple projects presented on subfolders of the dev.nds.ox.ac.uk domain. I.e. `https://dev.nds.ox.ac.uk/{{PROJECT_NAME}}/`

## Testing/Staging Server

**Location:** dev.nds.ox.ac.uk (163.1.198.206)

### Initial Server Setup

```
$ sudo apt autoremove
$ sudo apt autoclean
$ sudo apt update
$ sudo apt upgrade
```

Set the hostname (without needing a restart) by editing `sudo vi /etc/hostname` and putting in the FQDN (i.e. dev.nds.ox.ac.uk) after confirming that the local DNS server has been updated (request via MSD-IT Services). Also edit `/etc/hosts` and modify the 127.0.0.1 record with the same FQDN. These changes won't take effect until the server is restarted, but in the meantime we can activate this via  `sudo hostname dev.nds.ox.ac.uk`. 

`hostnamectl set-hostname dev.nds.ox.ac.uk` Should do much of the above too, but can't test that at this stage.

`sudo apt install vim` to fix `vi` to [behave as expected](https://askubuntu.com/questions/353911/hitting-arrow-keys-adds-characters-in-vi-editor).

#### SSH config

```
$ touch ~/.ssh/authorized_keys
$ vi .ssh/authorized_keys   # Put local keys into sshd
```
Need to edit sshd_config to disable password login, once we're sure that the key login is working (again). Note that login comes up as *unreachable* suggesting that we've got a path to home directory problem (and thus why the keys aren't being found)
```
$ sudo vi /etc/ssh/sshd_config
$ sudo systemctl restart sshd
$ tail -f /var/log/auth.log   # To see what is happening
```

```
$ ssh-keygen -t rsa -b 4096   # Generate server key
$ cat .ssh/id_rsa.pub   # Copy to Github
```

#### Python Basics
Notes from [Cope Docs](https://cope.nds.ox.ac.uk/docs/deployment.html) and [http://chrisstrelioff.ws/sandbox/2016/09/21/python_setup_on_ubuntu_16_04.html]()

Counter-intuitively we need to install system basics for the default python 2, so that we can then rely on using python 3 in the virtualenvs that all projects will be deployed in. *Trying to go to python 3 at a system level leads to confusion and pain - we've tried, more than once, time to learn and stop doing that!.*

```
$ sudo apt list --installed

$ sudo apt install python-virtualenv python-pip git
$ sudo apt install python3-virtualenv python3-pip git
# build-essentials (gcc, etc) and python-dev are included in the above

$ pip install --user --upgrade pip

$ pip --version
pip 9.0.1 from /home/carl/.local/lib/python2.7/site-packages (python 2.7)
```

#### PostFix (and Supervisor, NTP, Sqlite)

sqlite is so simple as to not need further mention, so this is mostly about Postfix.

`$ sudo apt install supervisor postfix ntp sqlite3 `

Postfix configured as:

* Type: Satellite System (all mail goes to a smarthost)
* System mail name: dev.nds.ox.ac.uk
* SMTP relay host (blank for none): smtp.ox.ac.uk

#### nginx 

This server will host multiple applications (typically a mix of static and python applications on Gunicorn processes). To simplify setup and scaling (without adding too much overhead to operation) there will be a nginx instance acting as a reverse proxy and SSL decoder, that will then reference a local nginx service on a specific local port for each application/project. Each project can therefore have its own nginx configuration and instance and thus be managed independently and not impact on other projects on the same system.

```
$ sudo apt install nginx

# UFW is enabled on this machine, so add initial rules for http and https
$ sudo ufw allow http
$ sudo ufw allow https
$ sudo ufw status
Status: active

To                         Action      From
--                         ------      ----
22                         ALLOW       Anywhere                  
80                         ALLOW       Anywhere                  
443                        ALLOW       Anywhere                  
22 (v6)                    ALLOW       Anywhere (v6)             
80 (v6)                    ALLOW       Anywhere (v6)             
443 (v6)                   ALLOW       Anywhere (v6)   
```

By default this enables a server on port 80, and serves a file from `/var/www/html/index.html`. Nginx configuration files at at `/etc/nginx` and the `default` config is in *sites-available*, linked to from *sites-enabled*.

```
# Create new projects folder and worker group
$ sudo mkdir -p /sites
$ sudo groupadd --system worker
$ sudo chown root:worker /sites/
$ sudo chmod 775 /sites/
$ sudo usermod -aG worker www-data
$ sudo usermod -aG worker carl
```

Modify the default configuration for nginx (`sudo vi sites-available/default`):

* Set server_name to FQDN for machine


#### VirtualEnvWrapper Installation
```
$ pip install --user virtualenvwrapper
```

And appending to .bashrc `vi ~/.bashrc`: 

```
# Setup VirtualEnvWrapper for this user
export WORKON_HOME=/sites/.virtualenvs
export PROJECT_HOME=/sites
source $HOME/.local/bin/virtualenvwrapper.sh
```

Then returning and:: `source ~/.bashrc`.

#### SSL Certificate

Help via:

* [https://help.ubuntu.com/lts/serverguide/certificates-and-security.html]()
* [https://wiki.it.ox.ac.uk/itss/CertificateService]()

```
$ cd ~/.ssh/
$ mkdir ssl-cert
$ cd ssl-cert/
$ vi website.ssl.cfg
$ openssl req -new -keyout private.pem -out dev.nds.csr -config ./website.ssl.cfg -batch -verbose -nodes

Using configuration from ./website.ssl.cfg
Generating a 2048 bit RSA private key
...................................+++
.+++
writing new private key to 'private.pem'
-----
```

#### Additionally

Including landscape-common for system information display (same as on cope.nds) on login `sudo apt install landscape-common` (note: this installs a tonne of extra python packages including *twisted*, *zope*, *openssl*, etc so isn't a small thing per se)

More login checks can be done via [Update-notifier](https://wiki.ubuntu.com/UpdateNotifier) (the display of which is located at `/etc/update-motd.d/`). At present there are very few in there compared with cope.nds.

`sudo apt install curl` - allows for testing via terminal/console server outputs (handy when you can't remotely access port 80/443 because of a firewall in your path).


### Initial Setup for Quod Project

Create the project and virtualenv structure:

```
$ mkproject -p /usr/bin/python3 quod
Already using interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in /sites/.virtualenvs/quod/bin/python3
Also creating executable in /sites/.virtualenvs/quod/bin/python
Installing setuptools, pkg_resources, pip, wheel...done.
virtualenvwrapper.user_scripts creating /sites/.virtualenvs/quod/bin/predeactivate
virtualenvwrapper.user_scripts creating /sites/.virtualenvs/quod/bin/postdeactivate
virtualenvwrapper.user_scripts creating /sites/.virtualenvs/quod/bin/preactivate
virtualenvwrapper.user_scripts creating /sites/.virtualenvs/quod/bin/postactivate
virtualenvwrapper.user_scripts creating /sites/.virtualenvs/quod/bin/get_env_details
Creating /sites/quod
Setting project for quod to /sites/quod

(quod) $ python --version   # Quick test to prove that python 3 is here. Note the virtualenv is automatically activated after starting project
Python 3.5.2

$ sudo useradd --system --gid worker --shell /bin/bash --home /sites/quod quod-app-user
```

Now get the project files and link to the local lib and bin folders for ease of reference.

```
$ git clone git@github.com:ouh-churchill/quod.git quod_repo
$ ln -s /sites/.virtualenvs/quod/lib ./lib
$ ln -s /sites/.virtualenvs/quod/bin ./bin

# Create the related nginx and gunicorn folders
$ mkdir -p var/log var/run etc/nginx/sites-available htdocs/media etc/gunicorn


$ cd quod_repo/
$ pip install -r requirements/staging.txt
```

