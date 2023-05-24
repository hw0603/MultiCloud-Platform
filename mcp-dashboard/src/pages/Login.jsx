import React from "react";
import { useStateContext } from "../contexts/ContextProvider";
import { Navigate } from "react-router-dom";

const Login = () => {
    const { isAuthorized } = useStateContext();

    return (
        <>
            {isAuthorized && (<Navigate to="/" replace={true}/>)}
            <h1>login page</h1>
        </>
    );
}

export default Login;