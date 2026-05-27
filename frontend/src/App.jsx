import "./App.css"
import { useState } from "react"

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts"

const API_URL = import.meta.env.VITE_API_URL

const COLORS = [
  "#3b82f6",
  "#22c55e",
  "#f97316",
  "#a855f7",
  "#06b6d4",
  "#eab308",
]

function App() {

  const [message, setMessage] = useState("")
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function sendMessage() {

    if (!message.trim()) return

    setLoading(true)
    setError("")
    setResponse(null)

    try {

      const res = await fetch(
        `${API_URL}/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message,
          }),
        }
      )

      if (!res.ok) {
        throw new Error("Backend request failed")
      }

      const data = await res.json()

      setResponse(data)

    } catch (err) {

      setError(
        "Something went wrong connecting to FleetOps AI."
      )

    } finally {

      setLoading(false)
    }
  }

  function handleKeyDown(e) {

    if (e.key === "Enter") {
      sendMessage()
    }
  }

  function renderChart() {

    if (!response?.chart) return null

    const chartData =
      response.chart.labels.map(
        (label, index) => ({
          name: label,
          value: response.chart.values[index],
        })
      )

    return (

      <>
        <div className="chart-container">

          <ResponsiveContainer
            width="100%"
            height={650}
          >

            <BarChart
              data={chartData}
              margin={{
                top: 30,
                right: 40,
                left: 95,
                bottom: 70,
              }}
              barCategoryGap="18%"
            >

              <CartesianGrid
                strokeDasharray="4 4"
                stroke="#7c8db5"
                opacity={0.35}
              />

              <XAxis
                dataKey="name"
                tick={{
                  fill: "#ffffff",
                  fontSize: 18,
                  fontWeight: "600",
                }}
                tickLine={false}
                axisLine={{
                  stroke: "#5b6b93",
                }}
                label={{
                  value: "Customer",
                  position: "insideBottom",
                  dy: 35,
                  fill: "#ffffff",
                  fontSize: 20,
                  fontWeight: "bold",
                }}
              />

              <YAxis
                tickFormatter={(value) =>
                  `$${value.toLocaleString()}`
                }
                tick={{
                  fill: "#ffffff",
                  fontSize: 17,
                  fontWeight: "500",
                }}
                tickLine={false}
                axisLine={{
                  stroke: "#5b6b93",
                }}
                label={{
                  value: "Revenue (USD)",
                  angle: -90,
                  position: "insideLeft",
                  dx: -70,
                  fill: "#ffffff",
                  fontSize: 22,
                  fontWeight: "bold",
                }}
              />

              <Tooltip
                cursor={{
                  fill: "rgba(255,255,255,0.08)",
                }}
                formatter={(value) => [
                  `$${Number(value).toLocaleString()}`,
                  "Revenue",
                ]}
                contentStyle={{
                  background:
                    "linear-gradient(145deg,#081738,#0b1d4d)",
                  border: "2px solid #2f6df6",
                  borderRadius: "18px",
                  color: "#ffffff",
                  boxShadow:
                    "0 0 25px rgba(47,109,246,0.45)",
                  padding: "18px",
                  fontSize: "18px",
                  fontWeight: "bold",
                }}
                labelStyle={{
                  color: "#ffffff",
                  fontSize: "22px",
                  fontWeight: "bold",
                  marginBottom: "10px",
                }}
                itemStyle={{
                  color: "#60a5fa",
                  fontSize: "18px",
                  fontWeight: "bold",
                }}
              />

              <Bar
                dataKey="value"
                radius={[14, 14, 0, 0]}
              >

                {chartData.map((entry, index) => (

                  <Cell
                    key={index}
                    fill={
                      COLORS[
                        index % COLORS.length
                      ]
                    }
                  />

                ))}

              </Bar>

            </BarChart>

          </ResponsiveContainer>

        </div>

        <div className="custom-legend">

          {chartData.map((item, index) => (

            <div
              className="legend-item"
              key={index}
            >

              <div
                className="legend-color"
                style={{
                  background:
                    COLORS[
                      index % COLORS.length
                    ],
                }}
              />

              <span>
                {item.name}: $
                {item.value.toLocaleString()}
              </span>

            </div>

          ))}

        </div>
      </>
    )
  }

  return (

    <div className="app">

      <div className="hero">

        <h1>
          FleetOps AI Assistant
        </h1>

        <p>
          AI-powered logistics analytics
          platform
        </p>

      </div>

      <div className="search-bar">

        <input
          type="text"
          placeholder="Ask something..."
          value={message}
          onChange={(e) =>
            setMessage(e.target.value)
          }
          onKeyDown={handleKeyDown}
        />

        <button
          onClick={sendMessage}
          disabled={loading}
        >

          {loading
            ? "Loading..."
            : "Send"}

        </button>

      </div>

      {error && (

        <div className="response-card">

          <h2>Error</h2>

          <p>{error}</p>

        </div>

      )}

      {response && (

        <div className="response-card">

          <h2>AI Response</h2>

          <p>{response.answer}</p>

          {response.mode === "kpi" &&
            response.kpi && (

              <div className="kpi-card">

                <h3>
                  KPI Metric
                </h3>

                <div className="kpi-number">

                  {typeof response.kpi ===
                  "number"
                    ? response.kpi.toLocaleString()
                    : response.kpi}

                </div>

              </div>

            )}

          {response.mode === "chart" &&
            renderChart()}

        </div>

      )}

    </div>
  )
}

export default App