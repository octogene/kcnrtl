#!/bin/sh
APP_PATH=`dirname "$0"`
PYTHONPATH="$PYTHONPATH:$APP_PATH" exec python2.7 $APP_PATH/kcnrtl/kcnrtl.py $*
 
