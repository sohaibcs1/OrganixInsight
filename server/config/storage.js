import fs from 'fs';
import path from "path";
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url)

const INDEX_TABLE_PATH = path.resolve(path.dirname(__filename), "../config/store/indexTable.json");
const SOURCE_COUNT_PATH = path.resolve(path.dirname(__filename), "../config/store/sourceCount.json");
const KEYWORDS_PATH = path.resolve(path.dirname(__filename), "../config/store/keywords.json");
const PROCESSED_KEYWORDS_PATH = path.resolve(path.dirname(__filename),"../config/store/processedKeywords.json");
const SETTINGS_PATH = path.resolve(path.dirname(__filename), '../config/store/settings.json');

if (!fs.existsSync(KEYWORDS_PATH)) {
  fs.writeFileSync(KEYWORDS_PATH, JSON.stringify([]));
}
if (!fs.existsSync(INDEX_TABLE_PATH)) {
  fs.writeFileSync(INDEX_TABLE_PATH, JSON.stringify({}));
}
if (!fs.existsSync(SOURCE_COUNT_PATH)) {
  fs.writeFileSync(SOURCE_COUNT_PATH, JSON.stringify({}));
}
if (!fs.existsSync(PROCESSED_KEYWORDS_PATH)) {
  fs.writeFileSync(PROCESSED_KEYWORDS_PATH, JSON.stringify({}));
}
if (!fs.existsSync(SETTINGS_PATH)) {
  fs.writeFileSync(SETTINGS_PATH, JSON.stringify({ summaryLength: 100, keywords: '', combinedSummryLength: 1000 }));
}
const paths = {
  keywords: KEYWORDS_PATH,
  indexTable: INDEX_TABLE_PATH,
  sourceCounts: SOURCE_COUNT_PATH,
  processedKeywords: PROCESSED_KEYWORDS_PATH,
  settings: SETTINGS_PATH
};

const Storage = {
  keywords: [],
  indexTable: {},
  sourceCounts: {},
  processedKeywords: {},
  settings: {},

  init() {
    this.keywords = JSON.parse(fs.readFileSync(KEYWORDS_PATH).toString("utf8"));
    this.indexTable = JSON.parse(fs.readFileSync(INDEX_TABLE_PATH).toString("utf8"));
    this.sourceCounts = JSON.parse(fs.readFileSync(SOURCE_COUNT_PATH).toString("utf8"));
    this.processedKeywords = JSON.parse(fs.readFileSync(PROCESSED_KEYWORDS_PATH).toString("utf8"));
    this.settings = JSON.parse(fs.readFileSync(SETTINGS_PATH).toString("utf8"));
  },

  saveAll() {
    fs.writeFileSync(KEYWORDS_PATH,JSON.stringify(this.keywords, null, 2));
    fs.writeFileSync(INDEX_TABLE_PATH,JSON.stringify(this.indexTable, null, 2));
    fs.writeFileSync(SOURCE_COUNT_PATH,JSON.stringify(this.sourceCounts, null, 2));
    fs.writeFileSync(PROCESSED_KEYWORDS_PATH,JSON.stringify(this.processedKeywords, null, 2));
  },

  save(type) {
    fs.writeFileSync(paths[type], JSON.stringify(this[type], null, 2));
  }
};

export default Storage;