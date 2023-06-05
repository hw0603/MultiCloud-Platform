import React, { useState } from "react";
import { Sidebar, Navbar } from "../components";
import { BasePage } from ".";

const Layout = () => {
    console.log("accessToken", localStorage.getItem("accessToken"));
    return (
        <div>
            <div className="flex relative dark:bg-main-dark-bg">
                <div className="w-72 fixed sidebar dark:bg-secondary-dark-bg bg-white ">
                    <Sidebar />
                </div>

                <div className="bg-main-bg min-h-screen md:ml-72 w-full flex flex-col">
                    <div className="fixed md:static bg-main-bg dark:bg-main-dark-bg navbar w-full border-b-2">
                        <Navbar />
                    </div>

                    <div className="flex-1">
                        <BasePage />
                    </div>
                </div>

            </div>
        </div>
    );
}

export default Layout;