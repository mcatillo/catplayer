# Generate AppImage

Install:

        python3.10 -m venv .menv
        source .menv/bin/activate
        pip install -r requirements_lin.txt
        pip install python-appimage

Run the command:

        python-appimage build app -p 3.10 catplayer-x86_64.AppImage
