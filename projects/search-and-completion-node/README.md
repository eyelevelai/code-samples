# Search and Completion Node.js Project

This is a Node.js demo of GroundX being used to inject information into a language model via a process called "Retreival Augmented Generation". This demo essentially allows you to ask questions about documents which are uploaded to GroundX. Visit [eyelevel.ai](https://www.eyelevel.ai/) for more information.

This is a local backend implementation which you can interface with via `curl`

# Features
When you send a query to this demo, the following happens:

- GroundX searches for the sections of documents which are relvent to your query
- GroundX retreivals and the original query are sent to a language model, allowing the model to answer the query.
- The model output is streamed to the client.

# Setup

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Node.js**: Install Node.js from [Node.js official website](https://nodejs.org/).
- **NPM**: Node.js comes with npm (Node Package Manager) pre-installed.
- **Yarn** (optional): If you prefer using Yarn, you can install it by following the instructions on [Yarn official website](https://yarnpkg.com/).

## Getting Started

### Setting up API Keys

This example assumes you have an API key set up for both OpenAI and GroundX. You can find your [OpenAI API keys here](https://platform.openai.com/account/api-keys) and your [GroundX API keys here](https://dashboard.groundx.ai/apikey)

They can be configured as an environment variable as follows:
```bash
% export OPEN_AI_API_KEY=************
% export GROUNDX_API_KEY=************
```

### Setting up a GroundX Bucket
GroundX is designed to allow language models to understand the content of complex human-centric documents. In order for this demo to work, you must have a GroundX "Content Bucket" with files uploaded.

Navigate to the [GroundX content page](https://dashboard.groundx.ai/content), create a new bucket, and upload your content to that bucket. Your bucket will automatically have an `ID` assigned to it. Saving that as an environment variable will allow this demo to access the content of that bucket.

```bash
% export GROUNDX_BUCKET_ID=************
```

### Install dependency

```bash
npm install
# or
yarn install
```

### Run locally

```bash
npm run start
# or
yarn run start
```
This will create a local server on [http://localhost:3000](http://localhost:3000) which is accessible via a post request to the `/search` endpoint.

### Test enpoint
Now that the server is running, you can get LLM responses grounded within uploaded documents via the following command.

```bash
curl -X POST http://localhost:3000/search -H "Content-Type: application/json" -d '{"query": "YOUR_QUERY_HERE"}'
```

# Core Components

If you would like to re-create this demo yourself, these are the demo enpont file:

- Entire application in **index.ts** file. Path: **src/index.ts**
