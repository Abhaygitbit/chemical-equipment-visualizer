import React, { useState } from 'react';
import './App.css';
import { equipmentAPI } from './services/api';
import { Pie, Bar } from 'react-chartjs-2';
// Chemical Equipment Visualizer - Main Application Component
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function App() {
  const [file, setFile] = useState(null);
  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file');
      return;
    }

    setLoading(true);
    try {
      const response = await equipmentAPI.uploadCSV(file);
      setDataset(response.data.data);
      alert('Upload successful!');
    } catch (error) {
      alert('Upload failed: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const response = await equipmentAPI.downloadPDF(dataset.id);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${dataset.id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      alert('Failed to download PDF');
    }
  };

  // Prepare chart data
  const typeData = dataset ? {
    labels: Object.keys(dataset.type_distribution || {}),
    datasets: [{
      data: Object.values(dataset.type_distribution || {}),
      backgroundColor: ['#667eea', '#764ba2', '#ff6b6b', '#4ecdc4', '#ffd93d']
    }]
  } : null;

  const avgData = dataset ? {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [{
      label: 'Average Values',
      data: [
        dataset.averages?.flowrate || 0,
        dataset.averages?.pressure || 0,
        dataset.averages?.temperature || 0
      ],
      backgroundColor: ['#667eea', '#764ba2', '#ff6b6b']
    }]
  } : null;

  return (
    <div className="App">
      <header className="app-header">
        <h1>🧪 Chemical Equipment Visualizer</h1>
        <p>Upload and analyze your equipment data</p>
      </header>

      <div className="content-container">
        {/* Upload Section */}
        {!dataset && (
          <div>
            <h2>Upload CSV File</h2>
            <div className="upload-box" onClick={() => document.getElementById('file-input').click()}>
              <div style={{fontSize: '64px'}}>📁</div>
              <h3>Click to select CSV file</h3>
              <input
                id="file-input"
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                style={{display: 'none'}}
              />
            </div>
            {file && <p style={{marginTop: '20px'}}>Selected: {file.name}</p>}
            <button onClick={handleUpload} disabled={loading}>
              {loading ? 'Uploading...' : 'Upload and Analyze'}
            </button>
          </div>
        )}

        {/* Dashboard */}
        {dataset && (
          <div>
            <h2>Dashboard - {dataset.filename}</h2>
            <button onClick={handleDownloadPDF} style={{marginBottom: '20px'}}>
              Download PDF Report
            </button>

            {/* Summary Cards */}
            <div className="summary-cards">
              <div className="summary-card">
                <h3>Total Equipment</h3>
                <p>{dataset.total_count}</p>
              </div>
              <div className="summary-card">
                <h3>Avg Flowrate</h3>
                <p>{dataset.averages?.flowrate?.toFixed(2)}</p>
              </div>
              <div className="summary-card">
                <h3>Avg Pressure</h3>
                <p>{dataset.averages?.pressure?.toFixed(2)}</p>
              </div>
              <div className="summary-card">
                <h3>Avg Temperature</h3>
                <p>{dataset.averages?.temperature?.toFixed(2)}</p>
              </div>
            </div>

            {/* Charts */}
            <div className="charts-container">
              <div className="chart-box">
                <h3>Equipment Type Distribution</h3>
                {typeData && <Pie data={typeData} />}
              </div>
              <div className="chart-box">
                <h3>Average Parameters</h3>
                {avgData && <Bar data={avgData} />}
              </div>
            </div>

            {/* Table */}
            <h3>Equipment Details</h3>
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
                {dataset.equipment_list?.map((eq) => (
                  <tr key={eq.id}>
                    <td>{eq.name}</td>
                    <td>{eq.type}</td>
                    <td>{eq.flowrate.toFixed(2)}</td>
                    <td>{eq.pressure.toFixed(2)}</td>
                    <td>{eq.temperature.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <button onClick={() => setDataset(null)} style={{marginTop: '20px'}}>
              Upload New File
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;