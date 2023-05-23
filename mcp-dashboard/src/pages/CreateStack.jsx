import React, { useLayoutEffect, useState } from "react";
import Button from "../components/Button";
import { useStateContext } from "../contexts/ContextProvider";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const CreateStack = () => {
    const { mainColor, base_url } = useStateContext();

    const createStackButtonClicked = () => {
        const stack_info = document.getElementById("stack_selectbox").value;
        const provider_info = document.getElementById("provider_selectbox").value;
        const stack_name = document.getElementById("stack_name").value;
        const stack_desc = document.getElementById("stack_desc").value;

        if (stack_info === ""){
            alert("스택 종류를 선택하세요.");
        }
        else if (provider_info === "") {
            alert("프로바이더 종류를 선택하세요.");
        }
        else if (stack_name === "") {
            alert("스택 이름을 입력하세요.");
        }
        else {
            if (stack_desc !== "") {
                axios.post(`${base_url}/api/v1/stacks`, {
                    stack_name: stack_name,
                    stack_type: stack_info,
                    description: stack_desc,
                })
                    .then((response) => {
                        console.log(response);
                    })
                    .catch((error) => {
                        console.log(error);
                    })
            }
        }
    }

    return (
        <>
            <div className="p-10">
                <div className="">
                    <div className="flex gap-4">
                        <select id="stack_selectbox" className="border-2 p-3 rounded-xl" defaultValue="">
                            <option value="">스택 종류 선택</option>
                            <option value="alb">alb</option>
                            <option value="bastion">bastion</option>
                            <option value="key_pair">key_pair</option>
                            <option value="nat_gateway">nat_gateway</option>
                            <option value="route_table">route_table</option>
                            <option value="security_group">security_group</option>
                            <option value="subnet">subnet</option>
                            <option value="vpc">vpc</option>
                        </select>

                        <select id="provider_selectbox" className="border-2 p-3 rounded-xl" defaultValue="">
                            <option value="">CSP 종류 선택</option>
                            <option value="aws">AWS</option>
                            <option value="gcp">GCP</option>
                            <option value="azure">Azure</option>
                            <option value="custom">Custom</option>
                        </select>
                    </div>

                    <div className="mt-10">
                        <div className="mb-6">
                            <p className="text-lg mb-1">스택 이름</p>
                            <input id="stack_name" type="text" className="border-1 p-3 rounded-xl w-80" />
                        </div>
                        <div className="mb-6">
                            <p className="text-lg mb-1">스택 설명</p>
                            <input id="stack_desc" type="text" className="border-1 p-3 rounded-xl w-80 h-40" />
                        </div>
                    </div>

                    <Button
                        bgColor={mainColor}
                        text="새 스택 생성"
                        color="white"
                        borderRadius="10px"
                        onClick={createStackButtonClicked}
                    />
                </div>
            </div>
        </>
    );
};

export default CreateStack;