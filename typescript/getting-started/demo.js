import { GroundXClient } from "groundx";;

import dotenv from 'dotenv'; 
dotenv.config();

if (!process.env.GROUNDX_API_KEY) {
  throw Error("You have not set a required environment variable (GROUNDX_API_KEY or OPENAI_API_KEY). Copy .env.sample and rename it to .env then fill in the missing values.");
}

const query = "YOUR QUERY";

// set to skip lookup, otherwise will be set to first result
let bucketId = 0;

// enumerated file type (e.g. docx, pdf)
// if not set, file type will be inferred from file extension
const fileType = null;

// optional name for file
const fileName = null;

// set to local file path or hosted URL to upload file
const uploadPath = "";

// initialize client
const client = new GroundXClient({
  apiKey: process.env.GROUNDX_API_KEY,
});


if (bucketId === 0) {
  // list buckets
  const bucketResponse = await client.buckets.list();

  if (!bucketResponse?.buckets?.count) {
    console.error("no results from buckets");
    console.log(bucketResponse?.buckets);
    throw Error("no results from GroundX bucket query");
  }

  bucketId = bucketResponse.buckets[0].bucketId;
}


if (uploadPath !== "") {
  const doc = {
    bucketId: bucketId,
    filePath: uploadPath,
  };
  if (fileName) {
    doc.fileName = fileName;
  }
  if (fileType) {
    doc.fileType = fileType;
  }

  // upload documents to GroundX
  let ingest = await client.ingest(
    [
      doc,
    ]
  );

  if (!ingest?.ingest?.processId) {
    console.error(ingest);
    throw Error("GroundX upload request failed");
  }

  // poll ingest status
  while (true) {
    ingest = await client.documents.getProcessingStatusById(ingest.ingest.processId);
    if (!ingest?.ingest?.status) {
        console.error(ingest);
        throw Error("GroundX ingest request failed");
    }

    if (ingest.ingest.status === "complete" || ingest.ingest.status === "error") {
        break;
    }

    console.log(ingest.ingest.status);
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}

if (query !== "") {
  // search
  const searchResponse = await client.search.content(
    bucketId,
    {
      query: query
    }
  );

  if (!searchResponse?.search?.text) {
    console.error("no results from search");
    console.log(searchResponse?.search);
    throw Error("no results from GroundX search query");
  }

  console.log(searchResponse.search.text);
}
