
const API_URL = import.meta.env.VITE_API_URL;

export async function sendMessage(userInput, conversationId = null) {
  const response = await fetch(`${API_URL}/chat/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_input: userInput,
      conversation_id: conversationId,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to send message");
  }

  return response.json();
}

export async function checkHealth() {
  const response = await fetch(`${API_URL}/`);

  if (!response.ok) {
    throw new Error("API is unavailable");
  }

  return response.json();
}
