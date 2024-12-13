"use client";

import { FC, useState, useEffect, useRef, ReactNode } from "react";
import { Box, TextField, Button, Typography, CircularProgress } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { TypingDot } from "./TypingDot/TypingDot";

type MessageType = "user" | "server";

interface Message {
  text: string | ReactNode;
  type: MessageType;
}

export const Chat: FC = () => {
  const [question, setQuestion] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isStreaming, setIsStreaming] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = (): void => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (): Promise<void> => {
    if (!question.trim()) return;

    const newMessages: Message[] = [...messages, { text: question, type: "user" }];
    setIsLoading(true);
    setMessages(newMessages);
    setQuestion("");
    setMessages([...newMessages, { text: <TypingDot />, type: "server" }]);

    const response = await fetch("/api/search", {
      method: "POST",
      body: JSON.stringify({ query: question }),
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let serverAnswer = "";
    setIsStreaming(true);

    if (reader) {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        serverAnswer += decoder.decode(value, { stream: true });
        // Add the streaming text to the UI in real-time
        setMessages([...newMessages, { text: serverAnswer, type: "server" }]);
      }
    }

    setIsStreaming(false);
    setIsLoading(false);
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "90vh",
        padding: 2,
      }}>
      <Box
        sx={{
          flex: 1,
          width: "100%",
          maxWidth: "600px",
          overflowY: "auto",
          padding: 2,
          border: "1px solid #ddd",
          borderRadius: 2,
          marginBottom: 2,
          backgroundColor: "#f9f9f9",
          position: "relative",
        }}>
        {messages.map((msg, index) => {
          const isLastMessage = index === messages.length - 1;
          return (
            <Box
              key={index}
              sx={{
                display: "flex",
                justifyContent: msg.type === "user" ? "flex-end" : "flex-start",
                marginY: 1,
              }}>
              <Box
                sx={{
                  display: "flex",
                  alignItems: "center",
                  padding: 1,
                  borderRadius: 2,
                  backgroundColor: msg.type === "user" ? "#1976d2" : "#e8eaee",
                  color: msg.type === "user" ? "#fff" : "#2c3359",
                  maxWidth: "80%",
                  wordBreak: "break-word",
                }}>
                <Typography component="span">
                  {msg.text}
                  {isLastMessage && isStreaming && msg.type === "server" && <TypingDot />}
                </Typography>
              </Box>
            </Box>
          );
        })}
        <div ref={messagesEndRef} />
      </Box>
      <Box
        sx={{
          display: "flex",
          flexDirection: "row",
          width: "100%",
          maxWidth: "635px",
        }}>
        <TextField
          variant="outlined"
          placeholder="Type your question..."
          value={question}
          sx={{ m: 0, flexGrow: 1 }}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSend();
            }
          }}
          disabled={isStreaming}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleSend}
          sx={{ marginLeft: 1, boxShadow: "none" }}
          disabled={isLoading || isStreaming}>
          {isLoading || isStreaming ? <CircularProgress color="inherit" size={20} /> : <SendIcon fontSize="medium" />}
        </Button>
      </Box>
    </Box>
  );
};
