import React, { useEffect, useLayoutEffect, useState } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";
import { useStateContext } from "../contexts/ContextProvider";
import {Button} from "../components";

const DeployLog = () => {
    const location = useLocation();
    const runId = location.state.task_id;
    const deployId = location.state.deploy_id;

    const { base_url, mainColor } = useStateContext();
    const [stackTypes, setStackTypes] = useState([]);

    useEffect(() => {
        console.log(runId, deployId);
        axios({
            method: "GET",
            url: `${base_url}/api/v1/deploy/${deployId}`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            }
        })
            .then((response) => {
                setStackTypes(response.data.detail_data.map(item => (
                    item.stack_type
                )))
            })
            .catch((error) => {
                console.log("error", error);
            })
    }, []);

    const getTaskLog = (task_id) => {
        axios({
            method: "GET",
            url: `${base_url}/api/v1/deploy/${runId}/logs/${task_id}`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            }
        })
            .then((response) => {
                console.log(response);
                document.getElementById("log").innerText = response.data;
            })
            .catch((error) => {
                console.log("error", error);
            })
    }

    return (
        <>
            <div>
                <div className="p-4 flex gap-4">
                    <select className="border-2 p-3 rounded-xl" id="stack_type" defaultValue="">
                        <option value="">스택 종류 선택</option>
                        {stackTypes.map((stack, idx) => (
                            <option key={idx} value={stack}>{stack}</option>
                        ))}
                    </select>

                    <select className="border-2 p-3 rounded-xl" id="task_type" defaultValue="">
                        <option value="">작업 선택</option>
                        <option value="check">check</option>
                        <option value="copy">copy</option>
                        <option value="storage_and_creds">storage_and_creds</option>
                        <option value="plan">plan</option>
                        <option value="apply">apply</option>
                        <option value="skip">skip</option>
                    </select>

                    <Button
                        bgColor={mainColor}
                        text="로그 조회"
                        color="white"
                        borderRadius="10px"
                        onClickFunc={() => {
                            const stack_type = document.getElementById("stack_type").value;
                            const task_type = document.getElementById("task_type").value;
                            getTaskLog(`${stack_type}.${task_type}`);
                        }}
                    />
                </div>

                <div className="bg-white border-2 rounded-xl mx-4 my-1 p-4">
                    <p id="log" className="text-xs">
                    </p>
                </div>
            </div>
        </>
    );
}

export default DeployLog;