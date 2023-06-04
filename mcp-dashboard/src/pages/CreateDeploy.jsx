import React, { useLayoutEffect, useState } from "react";
import Button from "../components/Button";
import { useStateContext } from "../contexts/ContextProvider";
import axios from "axios";
import { useLocation, useNavigate } from "react-router-dom";
import { Carousel } from "../components";

const CreateDeploy = () => {
    const { setCheckedInputs, parameters, mainColor, deployDetail, base_url } = useStateContext();
    const location = useLocation();
    const stacks = location.state.checkedInputs;
    const navigate = useNavigate();

    useLayoutEffect(() => {
        setCheckedInputs([]);
    }, []);

    const createDeploy = () => {
        const deploy_name = document.getElementById("deploy_name").value;
        const team = document.getElementById("team").value;
        const environment = document.getElementById("environment").value;
        const start_time = document.getElementById("start_time").value;
        const destroy_time = document.getElementById("destroy_time").value;

        const t = {
            deploy_name: deploy_name,
            team: team,
            environment: environment,
            start_time: start_time,
            destroy_time: destroy_time,
            deploy_detail: deployDetail
        }
        console.log("post parameters", t);

        if (deploy_name && team && environment) {
            axios({
                method: "POST",
                url: `${base_url}/api/v1/deploy`,
                headers: {
                    "Authorization": localStorage.getItem("accessToken")
                },
                data: {
                    deploy_name: deploy_name,
                    team: team,
                    environment: environment,
                    start_time: start_time,
                    destroy_time: destroy_time,
                    deploy_detail: deployDetail
                }
            })
                .then((response) => {
                    console.log(response);
                    alert("배포가 생성되었습니다.");
                    navigate("/deploy");

                })
                .catch((error) => {
                    console.log(error)
                })
        }
    }
    
    return (
        <>
            <div className="p-10 flex items-start gap-6 justify-around">
                <div>
                    <Carousel stacks={stacks} />
                </div>

                <div>
                    <div className="flex justify-between mb-2">
                        <div></div>
                        <Button
                            color="white"
                            bgColor={mainColor}
                            text="새 배포 생성"
                            borderRadius="10px"
                            onClickFunc={() => {
                                console.log(`button Clicked!!`, deployDetail);
                                createDeploy();
                            }}
                        />

                    </div>
                    <div className="border-2 w-400 bg-white p-6 rounded-2xl">
                        <div>
                            <p className="font-bold text-2xl">배포 정보</p>
                        </div>

                        <div className="mt-6 flex flex-col gap-4 py-2">
                            <div>
                                <p className="mb-1">Deploy Name</p>
                                <input id="deploy_name" type="text" className="border-2 p-2 rounded-xl w-full" />
                            </div>
                            <div>
                                <p className="mb-1">Team</p>
                                <input id="team" type="text" className="border-2 p-2 rounded-xl w-full" />
                            </div>
                            <div>
                                <p className="mb-1">Environment</p>
                                <input id="environment" type="text" className="border-2 p-2 rounded-xl w-full" />
                            </div>
                            <div>
                                <p className="mb-1">Start Time</p>
                                <input id="start_time" type="text" className="border-2 p-2 rounded-xl w-full" />
                            </div>
                            <div>
                                <p className="mb-1">Destroy Time</p>
                                <input id="destroy_time" type="text" className="border-2 p-2 rounded-xl w-full" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>


        </>
    );
};

export default CreateDeploy;