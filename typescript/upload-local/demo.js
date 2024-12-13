import { GroundXClient } from "groundx";;

import dotenv from 'dotenv'; 
dotenv.config();

if (!process.env.GROUNDX_API_KEY) {
  throw Error("You have not set a required environment variable (GROUNDX_API_KEY or OPENAI_API_KEY). Copy .env.sample and rename it to .env then fill in the missing values.");
}

// set to skip lookup, otherwise will be set to first result
let bucketId = 0;

// set to local file path to upload local file
const uploadPath = "";

if (uploadLocal === "") {
  throw Error("set the local file path")
}


// initialize client
const client = new GroundXClient({
  apiKey: process.env.GROUNDX_API_KEY,
});


if (bucketId === 0) {
  // list buckets
  const bucketResponse = await client.buckets.list();
  if (!bucketResponse?.buckets?.count) {
    console.error("no results from buckets");
    console.log(bucketResponse.buckets);
    throw Error("no results from GroundX bucket query");
  }

  bucketId = bucketResponse.buckets[0].bucketId;
}


// upload local documents to GroundX
let ingest = await client.ingest(
  [
    {
      bucketId: bucketId,
      filePath: uploadPath,
    },
  ]
);

if (!ingest?.ingest?.status) {
  console.error(ingest);
  throw Error("GroundX upload request failed");
}

// poll ingest status
while (ingest.ingest.status !== "complete" &&
  ingest.ingest.status !== "error" &&
  ingest.ingest.status !== "cancelled") {
  ingest = await client.documents.getProcessingStatusById(
    ingest.ingest.processId,
  );
  if (!ingest?.ingest?.status) {
    console.error(ingest);
    throw Error("GroundX upload request failed");
  }

  await new Promise((resolve) => setTimeout(resolve, 3000));
}
