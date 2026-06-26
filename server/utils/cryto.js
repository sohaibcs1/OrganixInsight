import crypto from "crypto";
import fs from "fs";
import config from "../config/index.js";

const hash = (text) =>
  crypto.pbkdf2Sync(text, config.hashSalt, 1000, 100, "sha512").toString("hex");
const matchHash = (encryptedText, matchText) =>
  encryptedText === hash(matchText);

const calculateFileHash = async (path) => {
  const hashSum = crypto.createHash("sha256");
  var stats = fs.statSync(path);

  await new Promise((resolve) =>
    fs
      .createReadStream(path, {
        start: 0,
        end: stats.size > 200 ? 200 : stats.size,
      })
      .on("data", (chunk) => {
        hashSum.update(chunk);
      })
      .on("end", () => {
        resolve();
      })
  );
  await new Promise((resolve) =>
    fs
      .createReadStream(path, {
        start: stats.size > 200 ? stats.size - 200 : 0,
        end: stats.size,
      })
      .on("data", (chunk) => hashSum.update(chunk))
      .on("end", () => resolve())
  );
  const hash = hashSum.digest("hex");
  return hash;
};

export { hash, matchHash, calculateFileHash };
