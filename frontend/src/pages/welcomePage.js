import React from "react";
import "../style.css"
import chartLogo2 from "../images/charterGo_img2.png"
import { useNavigate } from "react-router-dom";

import Button from '@mui/material/Button';

export default function WelcomePage(){

    const navigate = useNavigate();



    return (
        <main>
        <div className="welcomePage-container">
            <img src={chartLogo2} alt="Charter & Go logo" className="imageStyle" />
            
            {/*Greeting the user*/}
            <h2 className="welcomePage-h2-style">Welcome, Scan your receipt for reimbursement. Click below to get started</h2>
            <Button variant="outlined" className="welcomePage-style" onClick={() => navigate('../home')}>Begin</Button>
            
            

        </div>
        </main>
    )
}