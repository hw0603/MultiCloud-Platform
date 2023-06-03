import React, { useLayoutEffect, useState } from "react";
import Button from "../components/Button";
import { useStateContext } from "../contexts/ContextProvider";
import axios from "axios";
import { useLocation } from "react-router-dom";

const CreateDeploy = () => {
    const { setCheckedInputs } = useStateContext();
    const location = useLocation();
    const checkedInputs = location.state.checkedInputs;
    
    useLayoutEffect(() => {
        console.log("checkedInputs", checkedInputs);
        setCheckedInputs([]);
    }, []);

    return (
        <>
        </>
    );
};

export default CreateDeploy;