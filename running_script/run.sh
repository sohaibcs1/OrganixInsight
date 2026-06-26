#!/bin/bash

# Change directory to 3D_organixInsight
cd 3D_organixInsight/

# Run quasar dev in the background and detach it from the terminal
nohup quasar dev > quasar.log 2>&1 &

# Change directory to __server
cd server

# Run node server.js in the background and detach it from the terminal
nohup node server.js > server.log 2>&1 &

# Run upload.js in the background and detach it from the terminal
nohup node upload.js > upload.log 2>&1 &

# Change directory to ___node_modules
cd python-modules

# Run python app.py in the background and detach it from the terminal
nohup python app.py > app.log 2>&1 &

sleep 45

# Run python main.py in the background and detach it from the terminal
nohup python main.py > main.log 2>&1 &


cd flask_paraview

nohup python paraview.py > paraview.log 2>&1 &

cd ..

# ---- Start Cell Count Flask app
cd flask_cell_count
nohup python cellcount.py > flask_cell_count.log 2>&1 &
cd ..