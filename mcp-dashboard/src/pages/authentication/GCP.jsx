import React, { useLayoutEffect, useMemo, useState, useEffect } from "react";
import { useStateContext } from "../../contexts/ContextProvider";
import axios from "axios";
import { redirect, useNavigate } from "react-router-dom";
import { Table, Button } from "../../components";
import "../../components/Modal.css";
import { MdOutlineCancel } from "react-icons/md";
import { BsFillTrashFill } from "react-icons/bs"

const refresh = () => {
    window.location.replace("/GCP");
}

const Modal = () => {
    const { setIsModalOpen, mainColor, base_url } = useStateContext();
    const closeModal = () => {
        setIsModalOpen(false);
    }

    const createProvider = () => {
        const provider_team = document.getElementById("provider_team").value;
        const provider_environment = document.getElementById("provider_environment").value;
        const provider_GKJson = document.getElementById("provider_GKJson").value;

        if (provider_team && provider_environment && provider_GKJson) {

            axios({
                method: "POST",
                url: `${base_url}/api/v1/gcp`,
                headers: {
                    "Authorization": localStorage.getItem("accessToken")
                },
                data: {
                    team: provider_team,
                    environment: provider_environment,
                    gcloud_keyfile_json: {provider_GKJson},
                }
            })
                .then((response) => {
                    console.log(response);
                    closeModal();
                    alert("프로바이더가 생성되었습니다.");
                    refresh();
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
                        <p className="mb-1">GCloud Keyfile JSON</p>
                        <input id="provider_GKJson" type="text" className="border-2 p-2 rounded-xl w-full" />
                    </div>
                    
                    
                </div>
                <div className="mt-10">
                    <Button
                        color="white"
                        bgColor={mainColor}
                        text="새 프로바이더 생성"
                        borderRadius="10px"
                        onClickFunc={() => {
                            if (window.confirm("프로바이더를 생성하시겠습니까?"))
                            {
                                createProvider();
                            }
                        }}
                    />
                </div>
            </div>
        </div>
    );
}

const GCP = () => {
    const { mainColor, base_url, stacks, setStacks, isAuthorized, isModalOpen, setIsModalOpen } = useStateContext();
    const [providers, setProviders] = useState([]);

    const getProviderList = () => {
        axios({
            method: 'GET',
            url: `${base_url}/api/v1/gcp`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then((response) => {
                console.log(response)
                setProviders(response.data);
            })
            .catch((error) => {
                console.log("error", error);
            })
    }

    const deleteProvider = (id) => {
        axios({
            method: "DELETE",
            url: `${base_url}/api/v1/gcp/${id}`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then(() => {
                alert("선택한 프로바이더를 삭제하였습니다.")
                refresh();
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
                accessor: "gcloud_keyfile_json",
                Header: "GCloud Keyfile JSON"
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

            {isModalOpen && <Modal />}
        </>
    );
};

export default GCP;