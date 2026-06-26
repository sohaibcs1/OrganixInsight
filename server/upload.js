import express from 'express';
import cors from 'cors';
import multer from 'multer';
import path from 'path';
import { v4 as uuidv4 } from 'uuid';

const app = express();


const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads'); // Save files in the 'fixed' directory
  },
  filename: (req, file, cb) => {
    const uniqueName = `${file.originalname}`;
    cb(null, uniqueName);
  },
});

const upload = multer({
  storage,
  limits: {
    fileSize: 1024 * 1024 * 1024 * 100, // Limit the file size to 10GB (adjust as needed)
  },
  fileFilter: (req, file, cb) => {
    // Allow only image files (adjust file types as needed)
    // const allowedFileTypes = /jpeg|jpg|png|gif|czi/;
    const allowedFileTypes = /./;
    const extname = allowedFileTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedFileTypes.test(file.mimetype);
    if (extname && mimetype) {
      return cb(null, true);
    } else {
      cb('Error: Only image files are allowed.'); // Reject the file if it's not an image
    }
  },
});

app.use(cors());

app.post('/upload', upload.array('files'), (req, res) => {
  // Check if any files were uploaded
  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ error: 'No files were uploaded.' });
  }

  // Handle file upload logic here
  // You can access the uploaded files via req.files
  const headers = req.headers;
  console.log(req.files);

  // Create an array to store file URLs
  const fileUrls = req.files.map((file) => ({
    name: file.originalname,
    // url: `${file.path}`,
    url:file.originalname,
    headers: headers,
    size: file.size,
    mimetype: file.mimetype,
  }));

  // Respond with the file URLs
  res.json({ message: 'Files uploaded successfully', files: fileUrls });
});

const port = 7070;
app.listen(port, () => {
  console.log(`Server is running on http://134.197.75.35:${port}`);
});
