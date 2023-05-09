// import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import React, { useEffect } from 'react';
import Sidebar from './components/Sidebar';
import { AiTwotoneCloud } from "react-icons/ai";
import "./App.css";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <AiTwotoneCloud />
        <Sidebar />
      </BrowserRouter>
    </div>
  );
}

export default App;