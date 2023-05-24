import React from "react";
import { Routes, Navigate, Route } from "react-router-dom";
import { Home, Dashboard, Deploy, User, Stack, Log, OpLog, Setting, CreateStack, Login } from ".";

const BasePage = () => {
    return (
        <Routes>
            {/* <Route path="/" element={<Navigate to="/dashboard" />} /> */}
            <Route path="/" element={<Dashboard />} />

            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/stack" element={<Stack />} />
        </Routes>
    );
};

export default BasePage;