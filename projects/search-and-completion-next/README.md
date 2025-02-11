# Search and Completion Next.js Project

This is a Next.js demo of GroundX being used to inject information into a language model via a process called "Retreival Augmented Generation". Main component is **Chat.tsx** and endpoint in **/api/search** folder. This demo essentially allows you to ask questions about documents which are uploaded to GroundX. Visit [eyelevel.ai](https://www.eyelevel.ai/) for more information.

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

### Running On Prem

This project can be configured to interact with your on prem GroundX deployment by setting the `GROUNDX_BASE_URL` to your GroundX service URL.

If you'd like to user your own hosted LLM, you can set the `LLM_BASE_URL` to your hosted LLM endpoint. Your LLM must be compatible with the OpenAI chat API interface: https://platform.openai.com/docs/api-reference/chat

If you set `LLM_API_KEY`, the value will be added to the `Authorization: Bearer $LLM_API_KEY` header with every request.

### Setting up API Keys

This example assumes you have an API key set up for both OpenAI and GroundX. You can find your [OpenAI API keys here](https://platform.openai.com/account/api-keys) and your [GroundX API keys here](https://dashboard.groundx.ai/apikey)

Copy `.env.sample` to `.env` and add your API keys.

### Setting up a GroundX Bucket
GroundX is designed to allow language models to understand the content of complex human-centric documents. In order for this demo to work, you must have a GroundX "Content Bucket" with files uploaded.

Navigate to the [GroundX content page](https://dashboard.groundx.ai/content), create a new bucket, and upload your content to that bucket. Your bucket will automatically have an `ID` assigned to it. Saving that as the `GROUNDX_BUCKET_ID` environment variable will allow this demo to access the content of that bucket.

### Install dependencies

```bash
npm install
# or
yarn install
```

### Run locally

```bash
npm run dev
# or
yarn run dev
```

This will create a local server on [http://localhost:3000](http://localhost:3000).

# Core Components

If you would like to re-create this demo yourself, these are the demos major components:

- **Chat.tsx** Path: **src/app/chat/page.tsx**

- **Endpoint** Path: **src/app/api/search/route.ts**
