#!/bin/bash

NAME="quod_app"                                   # Name of the application
APP_ROOT=/sites/quod                              # Application root path
DJANGODIR=$APP_ROOT/quod_repo                     # Django project directory
SOCKFILE=$APP_ROOT/var/run/wsgi.socket            # we will communicte using this unix socket
USER=quod-app-user                                # the user to run as
GROUP=worker                                      # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=config.settings.staging    # which settings file should Django use
DJANGO_WSGI_MODULE=config.wsgi                    # WSGI module name
PID_FILE=$APP_ROOT/var/run/gunicorn.pid
ACCESS_LOG=$APP_ROOT/var/log/gunicorn_access.log
ERROR_LOG=$APP_ROOT/var/log/gunicorn_error.log
TIMEOUT=120                                       # Timeout in seconds. Set large to allow for debug to happen

echo "Starting $NAME as `/usr/bin/whoami`"

# Activate the virtual environment
cd $DJANGODIR
source $APP_ROOT/bin/activate
# export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
# export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(/usr/bin/dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=unix:$SOCKFILE \
  --timeout $TIMEOUT \
  --log-level=debug \
  --log-file=$ERROR_LOG \
  --access-logfile=$ACCESS_LOG \
  --error-logfile=$ERROR_LOG \
  --pid=$PID_FILE

#  --user=$USER --group=$GROUP \
