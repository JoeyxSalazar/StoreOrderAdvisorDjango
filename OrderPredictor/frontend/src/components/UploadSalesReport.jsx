// UploadSalesReport.jsx
import React, { useState } from 'react';
import axios from 'axios';
import './UploadSalesReport.css';

const UploadSalesReport = () => {
  const [file, setFile] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a file.");
      return;
    }
    setLoading(true);
    setError('');
    setReport(null);

    const formData = new FormData();
    formData.append('sales_report', file);

    try {
      const response = await axios.post('/api/process-report/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setReport(response.data);
    } catch (err) {
      setError("Error processing the file.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Sales Report</h2>
      <form onSubmit={handleSubmit}>
        <input 
          type="file" 
          accept=".csv, .xls, .xlsx" 
          onChange={handleFileChange} 
        />
        <button type="submit">Upload</button>
      </form>
      {loading && <p>Processing...</p>}
      {error && <p className="error">{error}</p>}
      
      {report && (
        <div className="report-container">
          <h3>Order Suggestions</h3>
          {/* Check if the response is in error format */}
          {report.error ? (
            <p className="error">{report.error}</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Total Sold</th>
                  <th>Suggested Order</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(report).map(([product, data]) => (
                  <tr key={product}>
                    <td>{product}</td>
                    <td>{data.total_sold}</td>
                    <td>{data.suggested_order}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
};

export default UploadSalesReport;
