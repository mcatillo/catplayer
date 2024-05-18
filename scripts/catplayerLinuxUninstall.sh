#!/bin/bash


printf "\n*****************************************\n"
printf " Uninstalling catplayer for linux users. "
printf "\n*****************************************\n"

printf "Decide the installation type between [global] or [local]\n that you want uninstall ([local] is the default one): "
read APP_INSTALLATION_TYPE

if [[ $APP_INSTALLATION_TYPE == 'global' ]]
then
    echo "You have chosen [global] option"
elif [[ $APP_INSTALLATION_TYPE == 'local' ]]
then
    echo "You have chosen [local] option"
elif [[ $APP_INSTALLATION_TYPE == '' ]]
then
    echo "The [local] option will be executed."
    APP_INSTALLATION_TYPE=local
else
    printf "\nNo proper uninstallation option specified\n"
fi

APP_NAME=$(grep "APP_NAME=" src/setup.py | sed 's/^.*=\"//' | sed 's/\"$//')
APP_USER=$(who am i | awk '{print $1}')
APP_CONFIG=/home/$APP_USER/.config/$APP_NAME

if [[ $APP_INSTALLATION_TYPE == 'global' ]]
then
    APP_EXE=/usr/bin/$APP_NAME
    APP_PATH=/usr/share/$APP_NAME
    APP_DESKTOP=/usr/share/applications
    APP_ICON=/usr/share/pixmaps

    rm -r $APP_PATH
    rm $APP_DESKTOP/$APP_NAME.desktop
    rm $APP_ICON/$APP_NAME.png
    rm $APP_EXE
    rm -r $APP_CONFIG

    unset APP_ICON
    unset SETUPPY
    unset APP_INSTALLATION_TYPE
    unset APP_OWNER
    unset APP_EXE
    unset APP_PATH
    unset APP_DESKTOP

    printf "\n*****************************************\n"
    printf " Everything has been deleted. "
    printf "\n*****************************************\n"

elif [[ $APP_INSTALLATION_TYPE == 'local' ]]
then
    APP_EXE=/home/$APP_USER/.local/bin/$APP_NAME
    APP_PATH=/home/$APP_USER/.local/share/$APP_NAME
    APP_DESKTOP=/home/$APP_USER/.local/share/applications

    rm -r $APP_PATH
    rm $APP_DESKTOP/$APP_NAME.desktop
    rm $APP_EXE
    rm -r $APP_CONFIG

    unset SETUPPY
    unset APP_INSTALLATION_TYPE
    unset APP_OWNER
    unset APP_EXE
    unset APP_PATH
    unset APP_DESKTOP


    printf "\n*****************************************\n"
    printf " Everything has been deleted. "
    printf "\n*****************************************\n"
else
    echo ""
fi

