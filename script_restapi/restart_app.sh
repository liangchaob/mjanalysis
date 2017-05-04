kill -9 $(lsof -i tcp:8088 -t)
nohup python app.py >>log.txt &