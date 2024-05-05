#!/bin/bash

echo ""
echo "*****************************************"
echo " Installation of catplayer for linux users."
echo "*****************************************"
echo ""

CATPLAYER_USER=$(who am i | awk '{print $1}')
PYTHONV=$(python3 -V)
PYTHONN=${PYTHONV:7:4}
CATPLAYER_EXE=/usr/bin/catplayer
CATPLAYER_PATH=/usr/share/catplayer
CATPLAYER_CONFIG=/home/$CATPLAYER_USER/.config/catplayer
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
    sudo -u $CATPLAYER_USER mkdir $CATPLAYER_CONFIG
    sudo -u $CATPLAYER_USER mkdir $CATPLAYER_CONFIG/config
    echo ""
    echo "*****************************************"
    echo " Copying files..."
    echo "*****************************************"
    echo ""
    cp -r ./logo $CATPLAYER_PATH/
    cp ./logo/catplayer_128x128.png $CATPLAYER_ICON/
    cp -r ./media $CATPLAYER_PATH/
    cp catplayer.desktop $CATPLAYER_DESKTOP/
    sudo -u $CATPLAYER_USER cp config/latest_config.json $CATPLAYER_CONFIG/config
    sudo -u $CATPLAYER_USER cp config/vocabulary.json $CATPLAYER_CONFIG/config

    echo ""
    echo "*****************************************"
    echo " Generating the executable..."
    echo "*****************************************"
    echo ""
    pyinstaller --noconsole --onefile --distpath="." --icon=logo/catplayer_128x128.ico --name=catplayer cli.py
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
    unset CATPLAYER_USER
    unset CATPLAYER_CONFIG
    rm -r .menv
    rm -r build
    rm catplayer.spec
    rm catplayer

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
