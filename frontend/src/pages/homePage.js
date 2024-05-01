import React from "react";
import NavBar from "../components/NavBar";
import Form from 'react-bootstrap/Form';
import { useState } from "react";
import Button from '@mui/material/Button';
import AWS from 'aws-sdk';


export default function HomePage(){


    // calling aws to send the receipt to the s3 buckets 
    AWS.config.update({
        region: '#ENTER REGION HERE',
        apiVersion: 'latest',
        credentials: {
          accessKeyId: '#ENTER ACCESS KEY HERE!!',
          secretAccessKey: '#ENTER SECRET KEY HERE!!'
        }
      })

    // useState responsible for file upload confirmation 
    const [result, setResult] = useState("");

    // useState responsible for file upload confirmation text color
    const [color, setColor] = useState("");

    const [selectedFile, setSelectedFile] = useState(null); // selected file


    const handleUpload = () => {
        if (!selectedFile){
            console.log("NO file, select one!!");
            setResult("No file selected. Try again");
            setColor("red");
            return;
        }

        const s3 = new AWS.S3(); // creating s3 bucket object

        // uploading receipt to s3 bucket
        s3.upload(
            {
                Bucket: 'PAST-BUCKET-NAME/upload',
                Key: selectedFile.name,
                Body: selectedFile,
            },
            (err,data) => {
                if(err){
                    console.error("Upload file Error",err);
                    setResult("Failed. Try again");
                    setColor("red");
                    return;
                }
                console.log("File upload Good!!", data);
                setColor("green");
                setResult("Success!");
            }
        );
    };

    const handleFileChange = (e) => {
        setSelectedFile(e.target.files[0]);
        console.log("the file is",selectedFile);
    }

    return (
        <div>
            <NavBar/>
            <div className="home-container">
            <h2 className="home-h2-style">File upload:</h2>
            <Form.Group controlId="formFile" className="mb-3">
                <Form.Control type="file" className="inputfile" id="file" name="file" onChange={handleFileChange}/>
            </Form.Group>
            <Button variant="outlined" className="upload-style" onClick={handleUpload}>Upload</Button>
            <br/>

            <p style={{'color': color}}>{result}</p>

            </div>
         
        </div>
    )
}