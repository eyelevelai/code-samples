import { chatCompletions as openAIChat } from "./openai";
import { chatCompletions as hostedChat } from "./hosted";

export async function chatCompletions(query: string, systemContext: string) {
  const openAiApiKey = process.env.OPENAI_API_KEY || "";
  const llmBaseUrl = process.env.LLM_BASE_URL || "";

  if (llmBaseUrl) {
    return await hostedChat(query, systemContext);
  } else if (openAiApiKey) {
    return await openAIChat(query, systemContext);
  } else {
    throw new Error(
      "No OpenAI or custom LLM environment variables set. Please provide either OPENAI_API_KEY or LLM_BASE_URL."
    );
  }
}