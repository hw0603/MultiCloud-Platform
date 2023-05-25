import React from "react";
import { Routes, Navigate, Route } from "react-router-dom";
import { Home, Dashboard, Deploy, User, Stack, Log, OpLog, Setting, CreateStack, Login } from ".";

const BasePage = () => {
    return (
        <Routes>
            <Route path="/" element={<Navigate to="/dashboard" />} />
            {/* <Route path="/" element={<Dashboard />} /> */}

            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/deploy" element={<Deploy />} />
            <Route path="/user" element={<User />} />
            <Route path="/log" element={<Log />} />
            <Route path="/opLog" element={<OpLog />} />
            <Route path="/setting" element={<Setting />} />
            <Route path="/stack" element={<Stack />} />
            <Route path="/stack/new" element={<CreateStack />} />

            {/* <Route path="AWS" element={<AWS />} /> */}

            <Route path="*" element={<Navigate to="/dashboard" />} />
        </Routes>
    );
};

export default BasePage;