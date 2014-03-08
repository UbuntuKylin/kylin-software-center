#!/bin/sh
backendPath="/usr/lib/python2.7/dist-packages/ubuntukylin-softwarecenter-daemon"
cd `dirname $0`
cp ./data/youkersystem /usr/bin/
echo "Copy systemdbus script to /usr/bin/"

cp ./data/youkersession /usr/bin/
echo "Copy sessiondbus script to /usr/bin/"


cp ./conf/com.ubuntukylin.softwarecenter.service /usr/share/dbus-1/system-services/
echo "Copy .service file to /usr/share/dbus-1/system-services/"

cp ./conf/com.ubuntukylin.softwarecenter.policy /usr/share/polkit-1/actions/
echo "Copy .policy file to /usr/share/polkit-1/actions/"

cp ./conf/com.ubuntukylin.softwarecenter.conf /etc/dbus-1/system.d/
echo "Copy .conf file to /etc/dbus-1/system.d/"

if [ ! -d "$backendPath" ]; then
    cp -rf ./dbus_service/ /usr/lib/python2.7/dist-packages/ubuntukylin-softwarecenter-daemon/
    echo "Copy backend folder to /usr/lib/python2.7/dist-packages/ubuntukylin-softwarecenter-daemon/"
else
    rm -rf "$bakendPath"
    cp -rf ./src /usr/lib/python2.7/dist-packages/ubuntukylin-softwarecenter-daemon/
    echo "Copy backend folder to /usr/lib/python2.7/dist-packages/ubuntukylin-softwarecenter-daemon/"
fi

rm -f /usr/bin/ubuntukylin-softwarecenter-daemon.py
echo "Remove /usr/bin/ubuntukylin-softwarecenter-daemon.py"

chmod +x "$backendPath"/start_systemdbus.py
ln -s "$backendPath"/start_systemdbus.py  /usr/bin/ubuntukylin-softwarecenter-daemon.py
echo "Build symbol link for service file"
echo "^^ Now, You can run the ubuntukylin software center!"
