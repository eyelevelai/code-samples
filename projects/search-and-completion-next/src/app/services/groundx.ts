import { GroundXClient } from "groundx";

const apiKey = process.env.GROUNDX_API_KEY as string;
const baseUrl = process.env.GROUNDX_BASE_URL as string;
const bucketID = process.env.GROUNDX_BUCKET_ID as string;

export const groundx = new GroundXClient({
  apiKey: apiKey,
  environment: `${baseUrl}/api`,
});

// https://docs.eyelevel.ai/reference/api-reference/search/content
export const groundxSearchContent = async (query: string) => {
  const response = await groundx.search.content(+bucketID, {
    query,
  });

  const searchContent = response?.search?.text?.substring(0, 2000);
  if (!searchContent) {
    throw new Error("No context found in the response");
  }

  return searchContent;
};
