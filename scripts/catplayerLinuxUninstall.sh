#!/bin/bash

echo ""
echo "*****************************************"
echo " Removing all files of catplayer..."
echo "*****************************************"
echo ""

CATPLAYER_USER=$(who am i | awk '{print $1}')

rm /usr/bin/catplayer
rm -r /usr/share/catplayer
rm /usr/share/applications/catplayer.desktop
rm /usr/share/pixmaps/catplayer_128x128.png
rm -r /home/$CATPLAYER_USER/.config/catplayer

unset CATPLAYER_USER

echo ""
echo "*****************************************"
echo " Done!"
echo "*****************************************"
echo ""

