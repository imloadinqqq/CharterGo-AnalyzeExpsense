import React, { useEffect, useState } from 'react';
import AWS from 'aws-sdk';
import { useNavigate } from 'react-router-dom';
import NavBar from "../components/NavBar";
import Button from '@mui/material/Button';


AWS.config.update({
  region: '#ENTER REGION HERE',
  accessKeyId: '#ENTER ACCESS KEY HERE',
  secretAccessKey: '#ENTER SECRET KEY HERE!!',
});

// create a new DocumentClient object to interact with DynamoDB
const docClient = new AWS.DynamoDB.DocumentClient();

function LastScans() {
  const [scans, setScans] = useState([]); 
  const [lastDeleted, setLastDeleted] = useState(null);
  const navigate = useNavigate();

  // // Function to navigate to the home page
  // const goToHome = () => {
  //   navigate('/home');
  // };

  // Fetch the scans from the DynamoDB table
  useEffect(() => {
    const params = {
      TableName: '#ENTER TABLE NAME HERE!!',
    };

    docClient.scan(params, (err, data) => {
        if (err) {
          console.error('Unable to scan the table:', JSON.stringify(err, null, 2));
        } else {
          setScans(data.Items);
        }
      });
    }, []);

  const sortById = () => {
    const sortedScans = [...scans].sort((a, b) => a.id - b.id);
    setScans(sortedScans);
  };

  const deleteScan = (id) => {
    const params = {
      TableName: '#ENTER TABLE NAME HERE!!',
      Key: {
        id: id
      }
    };

    docClient.delete(params, (err, data) => {
      if (err) {
        console.error('Unable to delete item:', JSON.stringify(err, null, 2));
      } else {
        const deletedScan = scans.find(scan => scan.id === id);
        setLastDeleted(deletedScan); // Add this line
        setScans(scans.filter(scan => scan.id !== id));
      }
    });
  };

  return (
    <div>
      <NavBar/>
      <div className='button-h1-div'>
      <h1 className='page-h2-style'>Your scanned receipt:</h1>
      <Button variant="outlined" className="sortButton-style" onClick={sortById}>sort by ID</Button>
      </div>
      {lastDeleted && <p>You deleted the scan with ID: {lastDeleted.id}</p>}
      <div className='table-outer-wrapper'>

      
      <div className='table-wrapper'>
      <table className="styled-table">
        <thead>
          <tr>
            <th style={{width: "3%"}}>ID</th>
            <th>Expenses</th>
            <th>Address</th>
            <th>Report Type</th>
            <th>Supplier ID</th>
            <th style={{width: "5%"}}>Delete</th>
          </tr>
        </thead>
        <tbody>
          {scans.map((scan, index) => (
            <tr key={index}>
              <td>{scan.id}</td>
              <td>{JSON.stringify(scan.expenses)}</td>
              <td>{scan.expenses && scan.expenses.map(expense => JSON.stringify(expense.address)).join(', ')}</td>
              <td>{scan.reportType}</td>
              <td>{scan.supplierId}</td>
              <td><button onClick={() => deleteScan(scan.id)}>Delete</button></td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
      </div>
    </div>
  );
}

export default LastScans;