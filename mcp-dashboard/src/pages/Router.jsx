import React from "react";
import { Routes, Route, Navigate, BrowserRouter } from "react-router-dom";
import { Login, Layout } from "./";
import { useStateContext } from "../contexts/ContextProvider";

const Router = () => {
  const { isAuthorized } = useStateContext();
  return (
    <div>
      {!isAuthorized && (<Navigate to="/login" replace={true} />)}
      <Routes>
        <Route exact path="/login" element={<Login />} />
        <Route path="*" element={<Layout />} />
      </Routes>
    </div>
  );
}

export default Router;