import React, { useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import "chart.js/auto";

function CSVUpload() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);

  const uploadCSV = async () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/upload/",
        formData,
        {
          auth: {
            username: "bhagyasri",
            password: "Test@1234"
          }
        }
      );
      setData(response.data);
    } catch (err) {
      console.error(err);
      alert("Upload failed. Is Django running?");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Chemical Equipment Visualizer</h2>

      <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={uploadCSV} style={{ marginLeft: "10px" }}>
        Upload
      </button>

      {data && (
        <>
          <h3>Summary</h3>
          <p>Total Equipment: {data.total_equipment}</p>
          <p>Avg Flowrate: {data.average_flowrate}</p>
          <p>Avg Pressure: {data.average_pressure}</p>
          <p>Avg Temperature: {data.average_temperature}</p>

          <h3>Equipment Distribution</h3>
          <Bar
            data={{
              labels: Object.keys(data.equipment_type_distribution),
              datasets: [
                {
                  label: "Count",
                  data: Object.values(data.equipment_type_distribution),
                  backgroundColor: "rgba(54, 162, 235, 0.6)",
                },
              ],
            }}
          />
        </>
      )}
    </div>
  );
}

export default CSVUpload;
