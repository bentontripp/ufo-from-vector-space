#!/bin/bash

VENV="$1"

function check_version {
    version=python --version 2>&1 | grep -Po 'Python \K.*'
    version=$(echo $version | grep -o '[^-]*$')
    major=$(echo $version | cut -d. -f1)
    minor=$(echo $version | cut -d. -f2)
    if ([ "$major" -ge 3 ] && [ "$minor" -ge 9 ])
    then
        true
        return
    else
        false
        return
    fi
}

if [ -d "$VENV" ]
then
    echo -e "Virtual environment exists"
    if [[ $OSTYPE == 'msys' ]]
    then
        echo "Activating Windows virtual environment $VENV..."
        source "$VENV/Scripts/activate"
        if check_version
        then
            echo "Ready."
        else
            deactivate
            echo -e "Python version below required 3.9. Exiting..."
        fi
    else
        echo "Script currently only written for Windows. Exiting..."
    fi
else
    echo -e "Virtual environment DOES NOT exist."
    read -p "Do you want to create a new environment $VENV (yes/no)? " yn
    if [[ $yn == 'yes' ]]
    then
        echo -e "Creating $VENV..."
        python -m venv "$VENV"
        source "$VENV/Scripts/activate"
        if check_version
        then
            echo "Installing Dependencies..."
            pip install numpy==1.23.2
            pip install pandas==1.4.3
            pip install beautifulsoup4==4.11.1
            pip install urllib3==1.26.11
            pip install requests==2.28.1
            pip install PyYAML==6.0
            pip install lxml==4.9.1
            pip install pipwin==0.5.2
            pipwin install gdal==3.4.3
            pipwin install fiona==1.8.21
            pip install geopandas==0.11.1
            pipwin install inpoly==0.1.2
            pip install matplotlib==3.5.3
            pip install Shapely==1.8.4
            pip install geocoder==1.38.1
            pip install ipykernel==6.15.1
        else
            deactivate
            echo -e "Python version below required 3.9. Exiting..."
        fi
    elif [[ $yn == 'no' ]]
    then
        echo -e "Exiting...";
    else
        echo -e "Invalid response. Exiting..."
    fi
fi

# Make executable using chmod +x <name>.sh
# Execute using . <script_name>.sh <venv_name>
# see https://stackoverflow.com/questions/7369145/activating-a-virtualenv-using-a-shell-script-doesnt-seem-to-work

