import express from 'express';
import http from 'http';
// import { Server as socket } from 'socket.io'
import { Server as socket } from 'socket.io'


const app = express();
const server = http.createServer(app);
const io = new socket(server);

// let client = null;
let client = null;
const initSocket = (window) => {
  console.log("init socket executes")
  io.on('connection', (c) => {
    
    client = c
  });
  io.on('disconnect', () => {
    client = null;

  });
  server.listen(6080);

}


export {
  initSocket,
  client
  
};

