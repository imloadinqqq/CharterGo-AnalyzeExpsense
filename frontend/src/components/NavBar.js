import React from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import chartLogo2 from "../images/charterGo_img2.png"
import { useNavigate } from "react-router-dom";


function ColorSchemesExample() {

  const navigate = useNavigate();

  return (
    <>
      <Navbar bg="light" data-bs-theme="light" className="navbar-container">
        <Container>
        <img src={chartLogo2} alt="Charter & Go logo" onClick={() => navigate('/')} className="navImage-style" />
          <Nav className="me-auto">
            <Nav.Link className='navLink-style' onClick={() => navigate('../home')}>Home</Nav.Link>
            <Nav.Link className='navLink-style' onClick={() => navigate('/scans')}>View Scans</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </>
  );
}

export default ColorSchemesExample;
