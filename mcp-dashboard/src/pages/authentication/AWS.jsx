import React, { useLayoutEffect, useMemo, useState, useEffect } from "react";
import { useStateContext } from "../../contexts/ContextProvider";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Table, Button } from "../../components";
import "../../components/Modal.css";
import { MdOutlineCancel } from "react-icons/md";

const Modal = () => {
    const { setIsModalOpen, mainColor, base_url } = useStateContext();
    const closeModal = () => {
        setIsModalOpen(false);
    }

    const createProvider = () => {
        const provider_team = document.getElementById("provider_team").value;
        const provider_environment = document.getElementById("provider_environment").value;
        const provider_keyID = document.getElementById("provider_keyID").value;
        const provider_region = document.getElementById("provider_region").value;
        const provider_profile = document.getElementById("provider_profile").value;
        const provider_sKey = document.getElementById("provider_sKey").value;

        if (provider_team && provider_environment && provider_keyID && provider_region && provider_profile) {

            axios({
                method: "POST",
                url: `${base_url}/api/v1/aws`,
                headers: {
                    "Authorization": localStorage.getItem("accessToken")
                },
                data: {
                    team: provider_team,
                    environment: provider_environment,
                    access_key_id: provider_keyID,
                    default_region: provider_region,
                    profile_name: provider_profile,
                    secret_access_key: provider_sKey,
                }
            })
                .then((response) => {
                    console.log(response)
                })
                .catch((error) => {
                    console.log(error)
                })
        }

    }

    return (
        <div className="absolute left-0 top-0 min-w-full min-h-full bg-black/50 flex justify-center items-center" id="modal_mask" onClick={closeModal}>
            <div className="m-10 bg-white w-1/3 p-10 rounded-2xl" onClick={(event) => {
                event.stopPropagation();
            }
            }>
                <div className="flex justify-between items-center">
                    <h1 className="font-bold text-xl">프로바이더 생성</h1>
                    <Button
                        icon={<MdOutlineCancel />}
                        color="rgb(153, 171, 180)"
                        bgHoverColor="light-gray"
                        size="2xl"
                        borderRadius="50%"
                        onClickFunc={closeModal}
                    />
                </div>

                <div className="mt-6 flex flex-col gap-4">
                    <div>
                        <p className="mb-1">Team</p>
                        <input id="provider_team" type="text" className="border-2 p-2 rounded-xl w-full" />
                    </div>
                    <div>
                        <p className="mb-1">Environment</p>
                        <input id="provider_environment" type="text" className="border-2 p-2 rounded-xl w-full" />
                    </div>
                    <div>
                        <p className="mb-1">Access Key ID</p>
                        <input id="provider_keyID" type="text" className="border-2 p-2 rounded-xl w-full" />
                    </div>
                    <div>
                        <p className="mb-1">Secret Access Key</p>
                        <input id="provider_sKey" type="text" className="border-2 p-2 rounded-xl w-full" />
                    </div>
                    <div>
                        <p className="mb-1">Default Region</p>
                        <input id="provider_region" type="text" className="border-2 p-2 rounded-xl w-full" />
                    </div>
                    <div>
                        <p className="mb-1">Profile Name</p>
                        <input id="provider_profile" type="text" className="border-2 p-2 rounded-xl w-full" />
                    </div>
                </div>
                <div className="mt-10">
                    <Button
                        color="white"
                        bgColor={mainColor}
                        text="새 프로바이더 생성"
                        borderRadius="10px"
                        onClickFunc={createProvider}
                    />
                </div>
            </div>
        </div>
    );
}

const AWS = () => {
    const { mainColor, base_url, stacks, setStacks, isAuthorized, isModalOpen, setIsModalOpen } = useStateContext();
    const navigate = useNavigate();
    const [providers, setProviders] = useState([]);
    // const [isModalOpen, setIsModalOpen] = useState(false);

    const columns = useMemo(
        () => [
            {
                accessor: "id",
                Header: "ID",
            },
            {
                accessor: "team",
                Header: "팀명"
            },
            {
                accessor: "environment",
                Header: "Environment"
            },
            {
                accessor: "default_region",
                Header: "Default region"
            },
            {
                accessor: "created_at",
                Header: "생성 날짜"
            }
        ], []
    );

    useLayoutEffect(() => {
        axios({
            method: 'GET',
            url: `${base_url}/api/v1/aws`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then((response) => {
                console.log(response.data);
                setProviders(response.data);
            })
            .catch((error) => {
                console.log("error", error);
            })
    }, []);

    return (
        <>
            <div className="px-10 py-5">
                <div className="flex justify-between p-3 m-3 border-b-2">
                    <div className="flex justfiy-center items-center text-2xl">관리 중인 프로바이더 목록</div>
                    <Button
                        color="white"
                        bgColor={mainColor}
                        text="새 프로바이더 생성"
                        borderRadius="10px"
                        onClickFunc={() => {
                            setIsModalOpen(!isModalOpen);
                        }}
                    />
                </div>

                <Table columns={columns} data={providers} />
            </div>

            {isModalOpen && <Modal />}
        </>
    );
};

export default AWS;