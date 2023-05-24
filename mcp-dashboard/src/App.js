import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Sidebar, Navbar } from './components';
import "./App.css";
import { useStateContext } from "./contexts/ContextProvider";
import { Home, Dashboard, Deploy, User, Stack, Log, OpLog, Setting, CreateStack, Login } from './pages';
import { AWS } from "./pages/authenticaion";

import { Router } from "./pages";

function App() {
  const { isAuthorized } = useStateContext();
  return (
    <>
      <BrowserRouter>
        <Router />
      </BrowserRouter>
    </>
    // <div className="App">
    //   <BrowserRouter>
    //     <div className="flex relative dark:bg-main-dark-bg">
    //       <div className="w-72 fixed sidebar dark:bg-secondary-dark-bg bg-white ">
    //         <Sidebar />
    //       </div>

    //       <div
    //         className={"dark:bg-main-dark-bg  bg-main-bg min-h-screen md:ml-72 w-full"}
    //       >

    //         <div className="fixed md:static bg-main-bg dark:bg-main-dark-bg navbar w-full border-b-2">
    //           <Navbar />
    //         </div>

    //         <div>
    //           <Routes>
    //             {/* home */}
    //             <Route path="/" element={<Navigate to="/dashboard" />} />

    //             <Route path="/dashboard" element={<Dashboard />} />
    //             <Route path="/deploy" element={<Deploy />} />
    //             <Route path="/user" element={<User />} />
    //             <Route path="/log" element={<Log />} />
    //             <Route path="/opLog" element={<OpLog />} />
    //             <Route path="/setting" element={<Setting />} />
    //             <Route path="/stack" element={<Stack />} />
    //             <Route path="/stack/new" element={<CreateStack />} />

    //             <Route path="AWS" element={<AWS />} />

    //             <Route path="*" element={<Navigate to="/dashboard" />} />
    //           </Routes>
    //         </div>
    //       </div>

    //     </div>
    //   </BrowserRouter>
    // </div>
  );
}

export default App;