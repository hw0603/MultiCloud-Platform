import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Sidebar, Navbar } from './components';
import "./App.css";
import { useStateContext } from "./contexts/ContextProvider";

import { Router } from "./pages";

function App() {
  const { isAuthorized } = useStateContext();
  return (
    <>
      <BrowserRouter>
        <Router />
      </BrowserRouter>
    </>
  );
}

export default App;