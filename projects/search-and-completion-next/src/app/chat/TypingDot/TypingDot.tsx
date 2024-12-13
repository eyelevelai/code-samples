import { keyframes } from "@emotion/react";
import Box from "@mui/material/Box/Box";

const typingDotAnimation = keyframes`
    0% { opacity: 0.1; }
    50% { opacity: 1; }
    100% { opacity: 0.5; }
`;

export const TypingDot = () => (
  <Box
    sx={{
      display: "inline-flex",
      alignItems: "center",
      mx: 1,
    }}>
    <Box
      sx={{
        width: 10,
        height: 10,
        borderRadius: "50%",
        backgroundColor: "black",
        animation: `${typingDotAnimation} 1s infinite`,
      }}
    />
  </Box>
);
