#!/bin/bash

printf "\n*****************************************\n"
printf " Installation of catplayer for linux users."
printf "\n*****************************************\n"

APP_NAME=$(grep "APP_NAME=" src/setup.py | sed 's/^.*=\"//' | sed 's/\"$//')
APP_USER=$(who am i | awk '{print $1}')
APP_CONFIG=/home/$APP_USER/.config/$APP_NAME

printf "Decide the installation type between [global] or [local]\n([local] is the default one and usually recommended): "
read APP_INSTALLATION_TYPE

if [[ $APP_INSTALLATION_TYPE == 'global' ]]
then
    echo "You have chosen [global] installation."
elif [[ $APP_INSTALLATION_TYPE == 'local' ]]
then
    echo "You have chosen [local] installation."
elif [[ $APP_INSTALLATION_TYPE == '' ]]
then
    echo "The [local] installation will be executed."
    APP_INSTALLATION_TYPE=local
else
    printf "\nThis installation choice is not possible!\n"
fi

if [[ $APP_INSTALLATION_TYPE == 'global' ]]
then
    APP_EXE=/usr/bin/$APP_NAME
    APP_PATH=/usr/share/$APP_NAME
    APP_DESKTOP=/usr/share/applications
    APP_ICON=/usr/share/pixmaps

    # Modify setup.py
    SETUPPY=$(cat src/setup.py | sed 's/INSTALLATION_TYPE=\"\w*\"//')
    printf "${SETUPPY[@]}" > src/setup.py
    printf '\nINSTALLATION_TYPE="global"' >> src/setup.py

    # Create environment
    python3 -m venv .menv
    source .menv/bin/activate
    pip install -r requirements_lin.txt

    printf "\n*****************************************\n"
    printf " Creating folders..."
    printf "\n*****************************************\n"

    mkdir $APP_PATH
    sudo -u $APP_USER mkdir $APP_CONFIG

    printf "\n*****************************************\n"
    printf " Creating Desktop file ..."
    printf "\n*****************************************\n"

    touch $APP_NAME.desktop
    echo "#!/usr/bin/env xdg-open" > $APP_NAME.desktop
    echo "[Desktop Entry]" >> $APP_NAME.desktop
    echo "Exec=$APP_NAME" >> $APP_NAME.desktop
    echo "Icon=$APP_NAME.png" >> $APP_NAME.desktop
    echo "Name=$APP_NAME" >> $APP_NAME.desktop
    echo "Type=Application" >> $APP_NAME.desktop
    echo "Comment=Basic video/music player app." >> $APP_NAME.desktop
    echo "Categories=AudioVideo;Player;Recorder;" >> $APP_NAME.desktop
    echo "Terminal=false" >> $APP_NAME.desktop
    echo "StartupNotify=false" >> $APP_NAME.desktop
    echo "Keywords=Player;Capture;DVD;Audio;Video;Server;Broadcast;" >> $APP_NAME.desktop

    printf "\n*****************************************\n"
    printf " Copying files and folders..."
    printf "\n*****************************************\n"

    cp ./data/logo/$APP_NAME.png $APP_ICON/
    cp -r ./data $APP_PATH/
    cp $APP_NAME.desktop $APP_DESKTOP/

    sudo -u $APP_USER cp -r config $APP_CONFIG/

    cp src/setup.py $APP_PATH/

    printf "\n*****************************************\n"
    printf " Generating the executable..."
    printf "\n*****************************************\n"

    pyinstaller --noconsole --onefile --distpath="." --name=$APP_NAME cli.py
    cp $APP_NAME $APP_EXE
    deactivate

    printf "\n*****************************************\n"
    printf " Removing temporary objects..."
    printf "\n*****************************************\n"

    rm -r build
    rm -r .menv
    rm $APP_NAME.spec
    rm $APP_NAME
    rm $APP_NAME.desktop

    unset APP_ICON
    unset SETUPPY
    unset APP_INSTALLATION_TYPE
    unset APP_OWNER
    unset APP_EXE
    unset APP_PATH
    unset APP_DESKTOP

elif [[ $APP_INSTALLATION_TYPE == 'local' ]]
then

    APP_EXE=/home/$APP_USER/.local/bin/$APP_NAME
    APP_PATH=/home/$APP_USER/.local/share/$APP_NAME
    APP_DESKTOP=/home/$APP_USER/.local/share/applications

    # Modify setup.py
    SETUPPY=$(cat src/setup.py | sed 's/INSTALLATION_TYPE=\"\w*\"//')
    printf "${SETUPPY[@]}" > src/setup.py
    printf '\nINSTALLATION_TYPE="local"' >> src/setup.py

    # Create environment
    python3 -m venv .menv
    source .menv/bin/activate
    pip install -r requirements_lin.txt

    printf "\n*****************************************\n"
    printf " Creating folders..."
    printf "\n*****************************************\n"

    sudo -u $APP_USER mkdir $APP_PATH
    sudo -u $APP_USER mkdir $APP_CONFIG

    printf "\n*****************************************\n"
    printf " Creating Desktop file ..."
    printf "\n*****************************************\n"

    sudo -u $APP_USER touch $APP_NAME.desktop
    sudo -u $APP_USER echo "#!/usr/bin/env xdg-open" > $APP_NAME.desktop
    sudo -u $APP_USER echo "[Desktop Entry]" >> $APP_NAME.desktop
    sudo -u $APP_USER echo "Exec=$APP_EXE" >> $APP_NAME.desktop
    sudo -u $APP_USER echo "Icon=$APP_PATH/data/logo/$APP_NAME.png" >> $APP_NAME.desktop
    sudo -u $APP_USER echo "Name=$APP_NAME" >> $APP_NAME.desktop
    sudo -u $APP_USER echo "Type=Application" >> $APP_NAME.desktop
    sudo -u $APP_USER echo "Comment=Basic video/music player app." >> $APP_NAME.desktop
    sudo -u $APP_USER echo "Categories=AudioVideo;Player;Recorder;" >> $APP_NAME.desktop
    sudo -u $APP_USER echo "Terminal=false" >> $APP_NAME.desktop
    sudo -u $APP_USER echo "StartupNotify=false" >> $APP_NAME.desktop
    sudo -u $APP_USER echo "Keywords=Player;Capture;DVD;Audio;Video;Server;Broadcast;" >> $APP_NAME.desktop

    printf "\n*****************************************\n"
    printf " Copying files and folders..."
    printf "\n*****************************************\n"

    sudo -u $APP_USER cp -r ./data $APP_PATH/
    sudo -u $APP_USER cp $APP_NAME.desktop $APP_DESKTOP/

    sudo -u $APP_USER cp -r config $APP_CONFIG/

    sudo -u $APP_USER cp src/setup.py $APP_PATH/

    printf "\n*****************************************\n"
    printf " Generating the executable..."
    printf "\n*****************************************\n"

    pyinstaller --noconsole --onefile --distpath="." --name=$APP_NAME cli.py
    sudo -u $APP_USER cp $APP_NAME $APP_EXE
    deactivate

    printf "\n*****************************************\n"
    printf " Removing temporary objects..."
    printf "\n*****************************************\n"

    rm -r build
    rm -r .menv
    rm $APP_NAME.spec
    rm $APP_NAME
    rm $APP_NAME.desktop

    unset SETUPPY
    unset APP_INSTALLATION_TYPE
    unset APP_OWNER
    unset APP_EXE
    unset APP_PATH
    unset APP_DESKTOP
else
    echo ""
fi

# Remodify setup.py
SETUPPY=$(cat src/setup.py | sed 's/INSTALLATION_TYPE=\"\w*\"//')
printf "${SETUPPY[@]}" > src/setup.py
printf '\nINSTALLATION_TYPE="local_dir"' >> src/setup.py

unset SETUPPY
unset APP_NAME
unset APP_USER
unset APP_CONFIG











