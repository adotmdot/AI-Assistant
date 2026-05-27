import { useState } from "react"
import axios from "axios"

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell
} from "recharts"

import "./App.css"

const API_URL = import.meta.env.VITE_API_URL

function App() {

  const [message, setMessage] = useState("")

  const [response, setResponse] = useState(null)

  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {

    if (!message.trim()) return

    try {

      setLoading(true)

      const res = await axios.post(
        `${API_URL}/chat`,
        {
          message
        }
      )

      setResponse(res.data)

    } catch (error) {

      console.error(error)

      setResponse({
        answer: "Something went wrong connecting to FleetOps AI.",
        mode: "error"
      })

    } finally {

      setLoading(false)
    }
  }

  const chartData = response?.chart
    ? response.chart.labels.map((label, index) => ({
        name: label,
        value: response.chart.values[index]
      }))
    : []

  return (

    <div className="app">

      <div className="hero">

        <h1>FleetOps AI Assistant</h1>

        <p>
          AI-powered logistics analytics platform
        </p>

      </div>

      <div className="search-bar">

        <input
          type="text"
          placeholder="Ask something..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />

        <button onClick={sendMessage}>
          Send
        </button>

      </div>

      {loading && (

        <div className="response-card">

          <h2>Analyzing Data...</h2>

          <p>Please wait while FleetOps processes your request.</p>

        </div>
      )}

      {response && !loading && (

        <div className="response-card">

          <h2>AI Response</h2>

          <p>{response.answer}</p>

          {/* KPI CARD */}

          {response.mode === "kpi" && response.kpi && (

            <div className="kpi-card">

              <h3>KPI Value</h3>

              <div className="kpi-number">

                {typeof response.kpi === "number"
                  ? response.kpi.toLocaleString()
                  : response.kpi}

              </div>

            </div>
          )}

          {/* CHART */}

          {response.mode === "chart" && (

            <div className="chart-container">

              <ResponsiveContainer
                width="100%"
                height={500}
              >

                <BarChart
                  data={chartData}
                  margin={{
                    top: 20,
                    right: 30,
                    left: 40,
                    bottom: 60
                  }}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="#6b7280"
                  />

                  <XAxis
                    dataKey="name"
                    tick={{ fill: "#ffffff", fontSize: 16 }}
                    label={{
                      value: "Customer",
                      position: "insideBottom",
                      offset: -20,
                      fill: "#ffffff",
                      fontSize: 20
                    }}
                  />

                  <YAxis
                    tick={{ fill: "#ffffff", fontSize: 14 }}
                    tickFormatter={(value) =>
                      `$${value.toLocaleString()}`
                    }
                    label={{
                      value: "Revenue (USD)",
                      angle: -90,
                      position: "insideLeft",
                      fill: "#ffffff",
                      fontSize: 20
                    }}
                  />

                  <Tooltip
                    formatter={(value) => [
                      `$${value.toLocaleString()}`,
                      "Revenue"
                    ]}
                    contentStyle={{
                      backgroundColor: "#111827",
                      border: "none",
                      borderRadius: "10px",
                      color: "#fff"
                    }}
                  />

                  <Bar
                    dataKey="value"
                    radius={[8, 8, 0, 0]}
                  >

                    {chartData.map((entry, index) => {

                      const colors = [
                        "#3b82f6",
                        "#22c55e",
                        "#f97316",
                        "#a855f7",
                        "#06b6d4",
                        "#eab308",
                        "#ef4444"
                      ]

                      return (
                        <Cell
                          key={`cell-${index}`}
                          fill={colors[index % colors.length]}
                        />
                      )
                    })}

                  </Bar>

                </BarChart>

              </ResponsiveContainer>

            </div>
          )}

        </div>
      )}

    </div>
  )
}

export default App