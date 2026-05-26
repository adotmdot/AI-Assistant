import { useState } from "react"
import axios from "axios"

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
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
                height={400}
              >

                <BarChart data={chartData}>

                  <CartesianGrid strokeDasharray="3 3" />

                  <XAxis dataKey="name" />

                  <YAxis />

                  <Tooltip />

                  <Bar dataKey="value" />

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