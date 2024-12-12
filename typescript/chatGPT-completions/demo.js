import { Groundx } from "groundx-typescript-sdk";
import OpenAI from 'openai';

import dotenv from 'dotenv'; 
dotenv.config();

if (!process.env.GROUNDX_API_KEY || !process.env.OPENAI_API_KEY) {
    throw Error("You have not set a required environment variable (GROUNDX_API_KEY or OPENAI_API_KEY). Copy .env.sample and rename it to .env then fill in the missing values.");
}

// GroundX Project ID or Bucket ID
// Found in your GroundX account
// OR by querying /project, /bucket
const groundxId = 0;

// Your question
const query = "YOUR QUERY HERE";

// Instructions sent to ChatGPT for completions
// You may want to change this
const instruction = "You are a helpful virtual assistant that answers questions using the content below. Your task is to create detailed answers to the questions by combining your understanding of the world with the content provided below. Do not share links.";


// Initialize the GroundX and OpenAI clients
const groundx = new Groundx({
    apiKey: process.env.GROUNDX_API_KEY,
});

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});


// Do a GroundX search
const result = await groundx.search.content({
    id: groundxId,
    query: query,
});
if (!result || !result.status || result.status != 200 || !result.data || !result.data.search) {
    console.error(result);
    throw Error("GroundX request failed");
}

if (!result.data.search.text) {
    console.error("no results from search");
    console.log(result.data.search);
    throw Error("no results from GroundX search");
}

// Access our suggested retrieved context
let llmText = result.data.search.text;

// Do an OpenAI completion with the search results
const completion = await openai.chat.completions.create({
    model: process.env.OPENAI_MODEL,
    messages: [
        {
            "role": "system",
            "content": `${instruction}
===
${llmText}
===
`
        },
        {"role": "user", "content": query},
    ],
});

if (!completion || !completion.choices || completion.choices.length == 0) {
    console.error(`\n\n\tempty result from OpenAI for query [${query}]\n\ntresult:\n\n\n`);
    console.log(completion);
    throw Error("OpenAI request failed")
}

console.log(`
    QUERY
    [${query}]
    
    SCORE
    [${result.data.search.score}]
    
    RESULT
    [${completion.choices[0].message.content}]
`);
