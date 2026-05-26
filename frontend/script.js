let analyticsChart = null


const API_URL =
  "http://127.0.0.1:8000/chat"

async function sendMessage() {

  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  const userMessage = input.value.trim();

  const welcome = document.querySelector(".welcome-container");

  if (welcome) {
    welcome.remove();
  }

  if (!userMessage) return;

  // User Bubble
  chatBox.innerHTML += `
    <div class="message user-message">
      <div class="message-content">
        ${userMessage}
      </div>
    </div>
  `;

  input.value = "";

  // Loading Bubble
  chatBox.innerHTML += `
    <div class="message bot-message" id="loading-message">
      <div class="message-content">

        <div class="typing">
          <span></span>
          <span></span>
          <span></span>
        </div>

      </div>
    </div>
  `;

  chatBox.scrollTop = chatBox.scrollHeight;

  try {

    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: userMessage
      })
    });

    const data = await response.json();

    if (data.mode === "chart") {

        const ctx = document
            .getElementById("analyticsChart")
            .getContext("2d")

        // destroy old chart
        if (analyticsChart) {
            analyticsChart.destroy()
        }

        analyticsChart = new Chart(ctx, {

            type: data.chart.type,

            data: {

                labels: data.chart.labels,

                datasets: [
                    {
                        label: data.answer,

                        data: data.chart.values,

                        backgroundColor: [
                            "#3b82f6",
                            "#2563eb",
                            "#1d4ed8",
                            "#60a5fa",
                            "#93c5fd"
                        ],

                        borderRadius: 10,

                        borderWidth: 0
                    }
                ]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        labels: {
                            color: "white"
                        }
                    }
                },

                scales: {

                    x: {
                        ticks: {
                            color: "white"
                        },

                        grid: {
                            color: "rgba(255,255,255,0.05)"
                        }
                    },

                    y: {
                        ticks: {
                            color: "white"
                        },

                        grid: {
                            color: "rgba(255,255,255,0.05)"
                        }
                    }
                }
            }
        })
    }


    // Remove loading
    document.getElementById("loading-message").remove();

    // AI Bubble
    chatBox.innerHTML += `
      <div class="message bot-message">
        <div class="message-content">
          ${data.answer}

          ${
            data.sources
              ? `
              <br><br>
              <div class="sources-container">

                ${data.sources
                  .map(
                    source => `
                      <div class="source-pill">
                        ${source}
                      </div>
                    `
                  )
                  .join("")}

</div>
            `
              : ""
          }
        </div>
      </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

  } catch (error) {

      console.error("Connection error:", error);

      document.getElementById("loading-message")?.remove();
    }
}


function quickPrompt(text) {

  document.getElementById("user-input").value = text;

  sendMessage();
}


document
  .getElementById("user-input")
  .addEventListener("keypress", function (e) {

    if (e.key === "Enter") {
      sendMessage();
    }
});