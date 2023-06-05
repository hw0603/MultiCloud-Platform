import React, { useEffect } from "react";
import { Routes, Route, Navigate, BrowserRouter, useNavigate } from "react-router-dom";
import { Login, Layout } from "./";
import { useStateContext } from "../contexts/ContextProvider";

const Router = () => {
  const { isAuthorized } = useStateContext();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthorized) {
      navigate("/login");
    }
  }, []);
  
  return (
    <div>
      <Routes>
        <Route exact path="/login" element={<Login />} />
        <Route path="*" element={<Layout />} />
      </Routes>
    </div>
  );
}

export default Router;