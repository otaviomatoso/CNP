@ECHO OFF

start cmd /c gradle
TIMEOUT 6
start cmd /k cd "mqtt-py\" ^& participant.py

@PAUSE
