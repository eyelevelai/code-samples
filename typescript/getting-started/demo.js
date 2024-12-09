import fs from 'fs';
import { Groundx } from "groundx-typescript-sdk";

import dotenv from 'dotenv'; 
dotenv.config();

if (!process.env.GROUNDX_API_KEY) {
  throw Error("You have not set a required environment variable (GROUNDX_API_KEY or OPENAI_API_KEY). Copy .env.sample and rename it to .env then fill in the missing values.");
}

const query = "YOUR QUERY";

// set to skip lookup, otherwise will be set to first result
let bucketId = 0;

// enumerated file type (e.g. docx, pdf)
// must be set to upload local or hosted
const fileType = "";

// must be set to upload local
const fileName = ""

// set to local file path to upload local file
const uploadLocal = "";

// set to hosted URL to upload hosted file
const uploadHosted = "";

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


if (uploadLocal !== "" && fileType !== "" && fileName !== "") {
  // upload local documents to GroundX
  let ingest = await groundx.documents.uploadLocal([
    {
      blob: fs.readFileSync(uploadLocal),
      metadata: {
        bucketId: bucketId,
        fileName: fileName,
        fileType: fileType,
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
}

if (uploadHosted !== "" && fileType !== "") {
  // upload hosted documents to GroundX
  let ingest = await groundx.documents.uploadRemote({
    documents: [
      {
        bucketId: bucketId,
        fileType: fileType,
        sourceUrl: uploadHosted,
      }
    ]
  });

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
}

if (query !== "") {
  // search
  const searchResponse = await groundx.search.content({
    id: bucketId,
    query: query
  });

  if (!searchResponse || !searchResponse.status || searchResponse.status != 200 ||
    !searchResponse.data || !searchResponse.data.search) {
    console.error(searchResponse);
    throw Error("GroundX search request failed");
  }

  if (!searchResponse.data.search.text) {
    console.error("no results from search");
    console.log(searchResponse.data.search);
    throw Error("no results from GroundX search query");
  }

  console.log(searchResponse.data.search.text);
}
