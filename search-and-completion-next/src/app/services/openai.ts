import OpenAI from "openai";
import { ChatCompletionChunk } from "openai/resources/chat/completions";
import { Stream } from "openai/streaming";

const openai = new OpenAI({
  apiKey: process.env.OPEN_AI_API_KEY,
});

const openAIStreamConfig = {
  model: "gpt-4o-mini",
  temperature: 0.4,
  top_p: 1,
  stop: ["==="],
  frequency_penalty: 0,
  presence_penalty: 0,
  max_tokens: 2000,
  stream: true,
  n: 1,
};

export const chatCompletions = async (query: string, systemContext: string) => {
  const stream = (await openai.chat.completions.create({
    ...openAIStreamConfig,
    messages: [
      {
        role: "system",
        content: `You are a helpful virtual assistant that answers questions using the content below.
                      Your task is to create detailed answers to the questions by combining
                      your understanding of the world with the content provided below. Do not share links.
                      ===
                      Context: ${systemContext} 
                      ===`,
      },
      { role: "user", content: query },
    ],
  })) as Stream<ChatCompletionChunk>;

  return stream;
};
