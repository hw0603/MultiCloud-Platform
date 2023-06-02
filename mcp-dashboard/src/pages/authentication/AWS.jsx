import React, { useLayoutEffect, useMemo, useState, useEffect } from "react";
import { useStateContext } from "../../contexts/ContextProvider";
import axios from "axios";
import { redirect, useNavigate } from "react-router-dom";
import { Table, Button, Modal } from "../../components";
import "../../components/Modal.css";
import { MdOutlineCancel } from "react-icons/md";
import { BsFillTrashFill } from "react-icons/bs"


const refresh = () => {
    window.location.replace("/AWS");
}

const ModalComponentCreateProvider = () => {
    const { setIsModalOpen, mainColor, base_url } = useStateContext();

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
                    console.log(response);
                    alert("프로바이더가 생성되었습니다.");
                    refresh();
                })
                .catch((error) => {
                    console.log(error)
                })
        }

    }
    return (
        <>
            <div>
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
                        onClickFunc={() => {
                            if (window.confirm("프로바이더를 생성하시겠습니까?")) {
                                createProvider();
                            }
                        }}
                    />
                </div>
            </div>
        </>
    )
}

const AWS = () => {
    const { mainColor, base_url, stacks, setStacks, isAuthorized, isModalOpen, setIsModalOpen } = useStateContext();
    const [providers, setProviders] = useState([]);

    const getProviderList = () => {
        axios({
            method: 'GET',
            url: `${base_url}/api/v1/aws`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then((response) => {
                setProviders(response.data);
            })
            .catch((error) => {
                console.log("error", error);
            })
    }

    const deleteProvider = (id) => {
        axios({
            method: "DELETE",
            url: `${base_url}/api/v1/aws/${id}`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then(() => {
                alert("선택한 프로바이더를 삭제하였습니다.")
                getProviderList();
            })
            .catch((error) => {
                console.log(error)
            })
    }

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
            },
            {
                accessor: "delete",
                Header: "삭제",
                Cell: tableProps => (
                    <div className="flex items-center justify-center">
                        <button onClick={() => {
                            if (window.confirm("선택한 프로바이더를 삭제하시겠습니까?")) {
                                deleteProvider(tableProps.data[tableProps.row.index].id)
                            }
                        }} style={{ color: "black", }}>
                            <BsFillTrashFill />
                        </button>
                    </div>
                ),
                minWidth: 140,
                width: 200,
            },
        ], []
    );

    useLayoutEffect(() => {
        getProviderList();
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

            {isModalOpen && <Modal title={"새 프로바이더 생성"}><ModalComponentCreateProvider /></Modal>}
        </>
    );
};

export default AWS;