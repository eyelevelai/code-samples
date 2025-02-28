import { NextResponse, NextRequest } from "next/server";
import { chatCompletions } from "@/app/services/llm";
import { groundxSearchContent } from "@/app/services/groundx";

const CorsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Content-Type": "text/event-stream;charset=utf-8",
  "Cache-Control": "no-cache, no-transform",
  "X-Accel-Buffering": "no",
};

export async function POST(req: NextRequest) {
  try {
    const { query } = await req.json();

    const searchContent = await groundxSearchContent(query);
    const res = await chatCompletions(query, searchContent);

    const llmBaseUrl = process.env.LLM_BASE_URL || "";

    if (llmBaseUrl) {
      return new Response(res, {
        headers: {
          ...CorsHeaders,
          "Content-Type": "text/plain; charset=utf-8",
        },
      });
    } else {
      const readableStream = new ReadableStream({
        async start(controller) {
          for await (const chunk of res) {
            controller.enqueue(new TextEncoder().encode(chunk.choices[0]?.delta?.content || ""));
          }
          controller.close();
        },
      });

      return new Response(readableStream, {
        headers: {
          ...CorsHeaders,
          "Content-Type": "text/plain; charset=utf-8",
        },
      });
    }
  } catch (err: any) {
    console.log(err, "message");
    return NextResponse.json({ error: err.message });
  }
}
