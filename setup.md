## update apt and install python deps
```shell
sudo apt update
sudo apt upgrade -y
sudo apt install git
sudo apt install python3 python3-pip -y
sudo apt install python3-venv -y
```

## generate ssh key pairs
```shell
ssh-keygen -t rsa -b 4096 -C "tech@duedil.ai"
```
Set `~/.ssh/id_rsa.pub` to github known publc keys for `ddtechu` user
## clone repo
```shell
git clone git@github.com:dcguim/duedeal-api.git
```
## run the app
```shell
cd duedeal-api 
python3 -m venv venv
source venv/bin/activate
pip install -r reqs.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
