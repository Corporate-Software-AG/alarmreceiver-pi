pip install -r requirements.txt

sudo cp services/alarmreceiver.service /lib/systemd/system

sudo systemctl daemon-reload
sudo systemctl enable alarmreceiver.service

echo 'export IOTHUB_DEVICE_CONNECTION_STRING="<CONNECTION_STRING>"' >> ~/.bashrc