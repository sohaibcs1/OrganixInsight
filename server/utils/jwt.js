import jwt from 'jsonwebtoken';
import config from '../config/index.js';

export const verifyToken = (token) => {
  let user;
  try {
    user = jwt.verify(token, config.hashSalt);
  } catch {
    user = null;
  }
  return user;
}