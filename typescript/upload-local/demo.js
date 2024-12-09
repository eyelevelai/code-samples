import fs from 'fs';
import { Groundx } from "groundx-typescript-sdk";

import dotenv from 'dotenv'; 
dotenv.config();

if (!process.env.GROUNDX_API_KEY) {
  throw Error("You have not set a required environment variable (GROUNDX_API_KEY or OPENAI_API_KEY). Copy .env.sample and rename it to .env then fill in the missing values.");
}

// set to skip lookup, otherwise will be set to first result
let bucketId = 0;

// enumerated file type (e.g. docx, pdf)
// must be set to upload local or hosted
const fileType = "";

// must be set to upload local
const fileName = ""

// set to local file path to upload local file
const uploadLocal = "";

if (uploadLocal === "") {
  throw Error("set the local file path")
}

if (fileType === "") {
  throw Error("set the file type to a supported enumerated type (e.g. txt, pdf)")
}

if (fileName === "") {
  throw Error("set a name for the file")
}


// initialize client
const groundx = new Groundx({
  apiKey: process.env.GROUNDX_API_KEY,
});


if (bucketId === 0) {
  // list buckets
  const bucketResponse = await groundx.buckets.list();
  if (!bucketResponse || !bucketResponse.status || bucketResponse.status != 200 ||
      !bucketResponse.data || !bucketResponse.data.buckets) {
    console.error(bucketResponse);
    throw Error("GroundX bucket request failed");
  }

  if (bucketResponse.data.buckets.count < 1) {
    console.error("no results from buckets");
    console.log(bucketResponse.data.buckets);
    throw Error("no results from GroundX bucket query");
  }

  bucketId = bucketResponse.data.buckets[0].bucketId;
}


// upload local documents to GroundX
let ingest = await groundx.documents.uploadLocal([
  {
    blob: fs.readFileSync(uploadLocal),
    metadata: {
      bucketId: bucketId,
      fileName: fileName,
      fileType: fileType,
      // optional metadata field
      // content is added to document chunks
      // fields are search during search requests
      // and returned in search results
      metadata: {
        key: "value"
      }
    },
  }
]);

if (!ingest || !ingest.status || ingest.status != 200 ||
  !ingest.data || !ingest.data.ingest) {
  console.error(ingest);
  throw Error("GroundX upload request failed");
}

// poll ingest status
while (ingest.data.ingest.status !== "complete" &&
  ingest.data.ingest.status !== "error" &&
  ingest.data.ingest.status !== "cancelled") {
  ingest = await groundx.documents.getProcessingStatusById({
    processId: ingest.data.ingest.processId,
  });
  if (!ingest || !ingest.status || ingest.status != 200 ||
    !ingest.data || !ingest.data.ingest) {
    console.error(ingest);
    throw Error("GroundX upload request failed");
  }

  await new Promise((resolve) => setTimeout(resolve, 3000));
}
