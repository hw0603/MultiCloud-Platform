import React, { useLayoutEffect, useMemo, useState } from "react";
import { Button, Table, Modal, ParameterCarousel } from "../components";
import { useNavigate } from "react-router-dom";
import { useStateContext } from "../contexts/ContextProvider";
import axios from "axios";
// import { BsFillTrashFill } from "react-icons/bs"
import { BsSearch } from "react-icons/bs"

const ModalComponentDeployParameter = ({ deployData }) => {
    console.log("deployData", deployData);
    return (
        <>
            <div className="flex justify-center items-center">
                <ParameterCarousel deployDetails={deployData} />
            </div>
        </>
    );
}

const Deploy = () => {
    const { mainColor, disabledColor, base_url, isModalOpen, setIsModalOpen, checkedInputs, setCheckedInputs } = useStateContext();
    const [deploys, setDeploys] = useState([]);
    const [deployData, setDeployData] = useState();
    const navigate = useNavigate();

    const getDeployList = () => {
        axios({
            method: 'GET',
            url: `${base_url}/api/v1/deploy`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then((response) => {
                console.log(response);
                setDeploys(response.data);
            })
            .catch((error) => {
                console.log("error", error);
            })
    }

    const getDeployInfo = (id) => {
        axios({
            method: "GET",
            url: `${base_url}/api/v1/deploy/${id}`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then((resp) => {
                console.log(resp);
                setDeployData(resp.data.detail_data);
                setIsModalOpen(true);
            })
            .catch((error) => {
                console.log("error", error);
            })
    }

    const columns = [
        {
            accessor: "deploy_id",
            Header: "ID",
        },
        {
            accessor: "deploy_name",
            Header: "배포명"
        },
        {
            accessor: "environment",
            Header: "Environment"
        },
        {
            accessor: "start_time",
            Header: "Start time"
        },
        {
            accessor: "destroy_time",
            Header: "Destroy time"
        },
        {
            accessor: "created_at",
            Header: "생성 날짜"
        },
        {
            accessor: "parameters",
            Header: "변수 확인",
            Cell: tableProps => (
                <div className="flex items-center justify-center">
                    <button onClick={() => {
                        // setDeployData(tableProps.data[tableProps.row.index]);
                        console.log(tableProps.data[tableProps.row.index].deploy_id);
                        getDeployInfo(tableProps.data[tableProps.row.index].deploy_id)

                    }} style={{ color: "black", }}>
                        <BsSearch />
                    </button>
                </div>
            ),
            minWidth: 140,
            width: 200,
        },
    ];

    useLayoutEffect(() => {
        getDeployList();
    }, []);

    return (
        <>
            <div className="px-10 py-5">
                <div className="flex justify-between p-3 m-3 border-b-2">
                    <div className="flex justfiy-center items-center text-2xl">관리 중인 배포 목록</div>
                    <div className="gap-4 flex">
                        <div>
                            <Button
                                color="white"
                                bgColor={mainColor}
                                text="새 배포 생성"
                                borderRadius="10px"
                                onClickFunc={() => {
                                    alert("스택을 선택하여 배포를 생성할 수 있습니다. 스택 페이지로 이동합니다.")
                                    navigate("/stack")
                                }}
                            />
                        </div>
                    </div>
                </div>

                <Table columns={columns} data={deploys} />
            </div>

            {isModalOpen && <Modal title="배포 세부사항" width="1/2"><ModalComponentDeployParameter deployData={deployData} /></Modal>}
        </>
    );
};

export default Deploy;