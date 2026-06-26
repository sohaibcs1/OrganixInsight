import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import { init as initiateDatabase } from './database/index.js';
import initControllers from './controllers/index.js';
import { initSocket } from './socket/index.js';


const app = express();
// initiate database initially
initiateDatabase();
initSocket();



app.use(bodyParser.json());
app.use(cors());

initControllers(app);

app.listen(8081, () => {
  console.log('app is listening on port ' + 8081);
});

// import express from 'express';
// import bodyParser from 'body-parser';
// import cors from 'cors';
// import { init as initiateDatabase } from './database/index.js';
// import initControllers from './controllers/index.js';
// import { initSocket } from './socket/index.js';

// const app = express();

// // ✅ Allow large JSON & URL-encoded payloads (up to 100MB)
// app.use(bodyParser.json({ limit: '500mb' }));
// app.use(bodyParser.urlencoded({ extended: true, limit:'500mb' }));

// // ✅ Enable CORS for all origins
// app.use(cors());

// // ✅ Initialize database and WebSocket
// initiateDatabase();
// initSocket();

// // ✅ Register routes/controllers
// initControllers(app);

// // ✅ Start server
// const PORT = 8081;
// app.listen(PORT, () => {
//   console.log(`✅ App is listening on port ${PORT}`);
// });
