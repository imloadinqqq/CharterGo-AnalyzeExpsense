
import React from "react";
import "./style.css"
import { Routes, Route, BrowserRouter } from "react-router-dom";
import WelcomePage from "./pages/welcomePage";
import NotFound from "./pages/NotFound";
import HomePage from "./pages/homePage";
import LastScans from "./pages/viewScans";


function App() {
  return (
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<WelcomePage/>}/>
      <Route path="/home" element={<HomePage/>}/>
      <Route path="/scans" element={<LastScans/>}/>
      <Route path="*" element={<NotFound/>}/>
    </Routes>
    </BrowserRouter>
  );
}

export default App;