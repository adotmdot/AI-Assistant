const API_URL =
  "https://fleetops-ai.greencoast-43a8316b.westus2.azurecontainerapps.io/chat";

async function sendMessage() {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  const userMessage = input.value;
  input.value = "";

  chatBox.innerHTML += `<div class="user">You: ${userMessage}</div>`;

  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: userMessage })
  });

  const data = await response.json();

  chatBox.innerHTML += `<div class="bot">AI: ${data.response}</div>`;
}
