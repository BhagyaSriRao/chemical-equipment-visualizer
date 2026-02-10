import React, { useState, useEffect } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import "./App.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

function App() {
  const [data, setData] = useState(null);
  const [file, setFile] = useState(null);
  const [history, setHistory] = useState([]);

  // Fetch last 5 uploaded datasets
  const fetchHistory = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/history/", {
        auth: { username: "bhagyasri", password: "Test@1234" },
      });
      setHistory(res.data);
    } catch (err) {
      console.error("Failed to fetch history:", err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  // Upload CSV
  const uploadCSV = async () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/upload/",
        formData,
        {
          auth: { username: "bhagyasri", password: "Test@1234" },
        }
      );
      setData(res.data);
      fetchHistory(); // refresh history after upload
    } catch (err) {
      alert("Upload failed. Is Django running?");
    }
  };

  // Chart Data
  const chartData =
    data && data.equipment_type_distribution
      ? {
          labels: Object.keys(data.equipment_type_distribution),
          datasets: [
            {
              label: "Equipment Count",
              data: Object.values(data.equipment_type_distribution),
              backgroundColor: "#4f9cff",
            },
          ],
        }
      : null;

  return (
    <div className="app">
      <h1>Chemical Equipment Visualizer</h1>
      <p className="subtitle">Hybrid Web + Desktop Analytics System</p>

      {/* Upload CSV */}
      <div className="upload-box">
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button onClick={uploadCSV}>Analyze CSV</button>
      </div>

      {/* Display current dataset */}
      {data && (
        <>
          <div className="stats">
            <div className="card">Total: {data.total_equipment}</div>
            <div className="card">Avg Flow: {data.average_flowrate}</div>
            <div className="card">Avg Pressure: {data.average_pressure}</div>
            <div className="card">Avg Temp: {data.average_temperature}</div>
          </div>

          <div className="chart-box">
            <Bar data={chartData} />
          </div>

          <div className="table-box">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Flowrate</th>
                  <th>Pressure</th>
                  <th>Temperature</th>
                </tr>
              </thead>
              <tbody>
                {data.table_data.map((row, i) => (
                  <tr key={i}>
                    <td>{row["Equipment Name"]}</td>
                    <td>{row.Type}</td>
                    <td>{row.Flowrate}</td>
                    <td>{row.Pressure}</td>
                    <td>{row.Temperature}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {/* History Section */}
      <div className="history-box">
        <h2>Last 5 Uploads</h2>
        <table>
          <thead>
            <tr>
              <th>Filename</th>
              <th>Total</th>
              <th>Avg Flow</th>
              <th>Avg Pressure</th>
              <th>Avg Temp</th>
              <th>PDF</th>
            </tr>
          </thead>
          <tbody>
            {history.map((h) => (
              <tr key={h.id}>
                <td>{h.filename}</td>
                <td>{h.total_equipment}</td>
                <td>{h.avg_flowrate}</td>
                <td>{h.avg_pressure}</td>
                <td>{h.avg_temperature}</td>
                <td>
                  {/* 🔹 Pass ID as query parameter to match backend */}
                  <a
                    href={`http://127.0.0.1:8000/api/download-pdf/?id=${h.id}`}
                    target="_blank"
                    rel="noreferrer"
                  >
                    PDF
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
