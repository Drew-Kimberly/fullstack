#Linux Server Configuration
##Overview
In this project, I configured and secured a clean Ubuntu 14.04 instance in AWS EC2.
I then installed and configured Apache web server and PostgreSQL, so that I could
deploy my Catalog Flask application. The following notes give a brief overview of
the software installed and configuration required:

##Notes

<b>IP Address:</b> 52.27.218.187 <br />
<b>SSH Port:</b> 2200 <br />
<b>User:</b> grader <br />
<b>Public URL:</b> http://ec2-52-27-218-187.us-west-2.compute.amazonaws.com/


<b>Additional Notes:</b>
- Remote connection as root user prohibited
    - Required edit to /etc/ssh/sshd_config


<b>Softwares Installed:</b>
- Apache2
	- Add catalog.wsgi application to /var/www/html
	- Edit /etc/apache2/sites-enabled/000-default.conf
	- Had to give 777 permission to static/img directory
- mod_wsgi - application handler
- PostgreSQL
	- No modifications to pg_hba.conf are necessary to prohibit remote connections
	- Add user "grader"
		- Grant all privileges for "catalog" database to user "grader"
	- Add user "catalog"
		- Grant SELECT, UPDATE, INSERT, and DELETE privileges on ALL TABLES AND SCHEMAS to user "catalog"
- Git
- apache2-mpm-prefork
- apache2-utils
- python-sqlalchemy
- python-psycopg2
- python-pip
- flask (installed w/ pip)
- sqlalchemy-utils (installed w/ pip)
- OAuth2Client (installed w/ pip)


<b>External Resources:</b>
- http://serverfault.com/questions/670646/adding-new-user-to-aws-ec2-permission-denied-publickey
- https://forums.aws.amazon.com/thread.jspa?threadID=104765
- https://forums.aws.amazon.com/thread.jspa?threadID=160352
- http://askubuntu.com/questions/323131/setting-timezone-from-terminal/323163
- https://www.digitalocean.com/community/tutorials/how-to-configure-the-apache-web-server-on-an-ubuntu-or-debian-vps
- https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps
- http://stackoverflow.com/questions/10861260/how-to-create-user-for-a-db-in-postgresql
- https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-14-04
- http://alex.nisnevich.com/blog/2014/10/01/setting_up_flask_on_ec2.html
- http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/
- https://discussions.udacity.com/t/error-when-logging-in-on-the-catalog-app/31738
    - *** solved what was by FAR the biggest headache of this proj ***
- https://discussions.udacity.com/t/psycopg2-programmingerror-permission-denied-for-sequence-item-id-seq/158306
- http://askubuntu.com/questions/27559/how-do-i-disable-remote-ssh-login-as-root-from-a-server
