# duedeal-api
## activating venv
```
python3 -m venv venv
source venv/bin/activate
pip install -r reqs.txt
```
## running the app with uvicorn
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
