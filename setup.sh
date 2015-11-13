#!/bin/sh

if ! which virtualenv > /dev/null ; then
    echo "Couldn't find virtualenv"
    exit 1
fi

if [ ! -f config.py ] ; then
    echo "Please copy config.py.dist to config.py and edit the settings accordingly (if appropriate)"
    exit 1
fi

echo "Configuring environment..."

[ ! -f env/bin/activate ] && virtualenv env
. env/bin/activate

pip install -qr requirements.txt

touch tmp/restart.txt

echo "Setup complete."
