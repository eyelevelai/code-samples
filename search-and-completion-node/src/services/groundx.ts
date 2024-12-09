import { Groundx } from "groundx-typescript-sdk";

const bucketID = process.env.GROUNDX_BUCKET_ID as string;
const apiKey = process.env.GROUNDX_API_KEY as string;

export const groundx = new Groundx({
  apiKey: apiKey,
});

// https://documentation.groundx.ai/reference/Search/Search_content
export const groundxSearchContent = async (query: string) => {
  const response = await groundx.search.content({
    id: +bucketID,
    query,
  });

  const searchContent = response?.data?.search?.text?.substring(0, 2000);
  if (!searchContent) {
    throw new Error("No context found in the response");
  }

  return searchContent;
};
