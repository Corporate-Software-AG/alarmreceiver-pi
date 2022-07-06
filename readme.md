sudo pip install -r requirements.txt

sudo cp services/alarmreceiver.service /lib/systemd/system

sudo systemctl daemon-reload
sudo systemctl enable alarmreceiver.service