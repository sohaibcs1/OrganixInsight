// import axios from 'axios';

// const REAL_TIME = window.REAL_TIME;

// export {
//   REAL_TIME
// };

// const API = (path, jsonData = {}) => {
//   const data = JSON.stringify(jsonData);
//   return axios.post(`http://134.197.75.35:8081/${path}`, { data }).then(res => res.data)
// };
// export default API;

import axios from 'axios';

// Use window.location.hostname to determine the correct base URL
const BASE_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:8081'  // Use localhost in development
  : `http://${window.location.hostname}:8081`; // Use dynamic IP in production

const API = (path, jsonData = {}) => {
  const data = JSON.stringify(jsonData);
  return axios.post(`${BASE_URL}/${path}`, { data }).then(res => res.data);
};

export default API;



