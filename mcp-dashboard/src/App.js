import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Sidebar, Navbar } from './components';
import "./App.css";
import { useStateContext } from "./contexts/ContextProvider";
import { Home, Dashboard, Deploy, User, Stack, Log, OpLog, Setting } from './pages';
import { AWS } from "./pages/authenticaion";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <div className="flex relative dark:bg-main-dark-bg">
          <div className="w-72 fixed sidebar dark:bg-secondary-dark-bg bg-white ">
            <Sidebar />
          </div>

          <div
            className={"dark:bg-main-dark-bg  bg-main-bg min-h-screen md:ml-72 w-full"}
          >

            <div className="fixed md:static bg-main-bg dark:bg-main-dark-bg navbar w-full border-b-2">
              <Navbar />
            </div>

            <div>
              <Routes>
                {/* home */}
                <Route path="/" element={<Home />} />
                <Route path="/home" element={<Home />} />

                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/deploy" element={<Deploy />} />
                <Route path="/user" element={<User />} />
                <Route path="/log" element={<Log />} />
                <Route path="/opLog" element={<OpLog />} />
                <Route path="/setting" element={<Setting />} />
                <Route path="/stack" element={<Stack />} />

                <Route path="AWS" element={<AWS />} />
              </Routes>
            </div>
          </div>

        </div>
      </BrowserRouter>
    </div>
  );
}

export default App;