#!/bin/bash

echo ""
echo "*****************************************"
echo " Installation of catplayer for linux users."
echo "*****************************************"
echo ""

PYTHONV=$(python3 -V)
PYTHONN=${PYTHONV:7:4}
CATPLAYER_EXE=/usr/bin/catplayer
CATPLAYER_PATH=/usr/share/catplayer
CATPLAYER_DESKTOP=/usr/share/applications
CATPLAYER_ICON=/usr/share/pixmaps

if [ $PYTHONN == '3.10' ]
then
    python3 -m venv .menv
    source .menv/bin/activate
    pip install -r requirements_lin.txt

    echo ""
    echo "*****************************************"
    echo " Creating folders..."
    echo "*****************************************"
    echo ""
    mkdir $CATPLAYER_PATH
    cp -r ./logo $CATPLAYER_PATH/
    cp ./logo/logo_dot.png $CATPLAYER_ICON/
    cp -r ./src $CATPLAYER_PATH/
    cp catplayer.desktop $CATPLAYER_DESKTOP/

    echo ""
    echo "*****************************************"
    echo " Generating the executable..."
    echo "*****************************************"
    echo ""
    pyinstaller --noconsole --onefile --distpath="." --icon=logo/logo_dot.ico --name=catplayer cli.py
    cp catplayer $CATPLAYER_EXE
    deactivate

    echo ""
    echo "*****************************************"
    echo " Removing temporary objects..."
    echo "*****************************************"
    echo ""
    unset PYTHONN
    unset CATPLAYER_EXE
    unset CATPLAYER_PATH
    unset CATPLAYER_DESKTOP
    unset CATPLAYER_ICON
    rm -r .menv
    rm -r build
    rm catplayer.spec

    echo ""
    echo "*****************************************"
    echo " catplayer installed!"
    echo "*****************************************"
    echo ""
else
    unset PYTHONN
    unset CATPLAYER_EXE
    unset CATPLAYER_PATH
    unset CATPLAYER_DESKTOP
    unset CATPLAYER_ICON
    echo ""
    echo "************************************************************************"
    echo " Python 3.10 is required! Please install it and retry to run this script."
    echo "************************************************************************"
    echo ""
fi
