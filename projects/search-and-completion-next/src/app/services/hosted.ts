import {
  ChatCompletionCreateParamsBase,
  ChatCompletionMessageParam,
} from "openai/resources/chat/completions";

const LLM_BASE_URL =
  `${process.env.LLM_BASE_URL}/chat/completions`;

interface ChatCompletionOptions {
  model?: string;
  temperature?: number;
  top_p?: number;
  stop?: string[];
  frequency_penalty?: number;
  presence_penalty?: number;
  max_tokens?: number;
  n?: number;
}

/**
 * Call an endpoint that behaves similarly to OpenAI's /chat/completions,
 * but at a custom URL (LLM_BASE_URL).
 */
export async function chatCompletions(
  query: string,
  systemContext: string,
  options: ChatCompletionOptions = {}
) {
  const messages: ChatCompletionMessageParam[] = [
    {
      role: "system",
      content: `You are a helpful virtual assistant that answers questions using the content below.
                Your task is to create detailed answers to the questions by combining
                your understanding of the world with the content provided below. Do not share links.
                ===
                Context: ${systemContext}
                ===`,
    },
    {
      role: "user",
      content: query,
    },
  ];

  const requestBody: ChatCompletionCreateParamsBase = {
    model: options.model ?? "gpt-4o",
    messages,
    temperature: options.temperature ?? 0.4,
    top_p: options.top_p ?? 1,
    stop: options.stop ?? ["==="],
    frequency_penalty: options.frequency_penalty ?? 0,
    presence_penalty: options.presence_penalty ?? 0,
    max_tokens: options.max_tokens ?? 2000,
    n: options.n ?? 1,
  };

  const response = await fetch(LLM_BASE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.LLM_API_KEY || ""}`,
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    throw new Error(
      `LLM request failed with status ${response.status}: ${response.statusText}`
    );
  }

  const data = await response.json();
  return data;
}
