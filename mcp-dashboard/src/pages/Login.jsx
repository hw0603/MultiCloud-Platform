import React, { useState, useEffect } from "react";
import { useStateContext } from "../contexts/ContextProvider";
import { Navigate } from "react-router-dom";
import { Button } from "../components";
import { AiTwotoneCloud } from "react-icons/ai";
import axios from "axios";

const Login = () => {
    const { isAuthorized, setIsAuthorized, mainColor, base_url } = useStateContext();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        submitForm();
    }

    const submitForm = () => {
        axios({
            method: 'POST',
            url: `${base_url}/api/v1/auth/access_token`,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data: {
                username: username,
                password: password,
            }
        })
            .then((response) => {
                if (response.data.access_token) {
                    localStorage.setItem("accessToken", `${response.data.token_type} ${response.data.access_token}`);
                }
                setIsAuthorized(!isAuthorized);
            })
            .catch((error) => {
                console.log("error :", error)
            })
    }

    return (
        <>
            {isAuthorized && (<Navigate to="/" replace={true} />)}
            <div className="flex justify-center items-center flex-wrap w-full min-h-screen dark:bg-main-dark-bg bg-main-bg">
                <div>
                    <div className="flex justify-between items-stretch flex-col gap-y-4">
                        <div className="flex items-center gap-2">
                            <AiTwotoneCloud className="text-2xl" /><span className="text-2xl">Multi-Cloud Platform</span>
                        </div>
                        <form onSubmit={handleSubmit} className="flex flex-col gap-y-4">
                            <input className="border-2 p-3 rounded-xl" type="text" placeholder="username" value={username} onChange={(e) => {
                                setUsername(e.target.value);
                            }} />
                            <input className="border-2 p-3 rounded-xl" type="password" placeholder="password" value={password} onChange={(e) => {
                                setPassword(e.target.value);
                            }} />
                            <Button
                                color="white"
                                bgColor={mainColor}
                                text="로그인"
                                borderRadius="10px"
                                type="submit"
                            />
                        </form>

                    </div>
                </div>
            </div>
        </>
    );
}

export default Login;