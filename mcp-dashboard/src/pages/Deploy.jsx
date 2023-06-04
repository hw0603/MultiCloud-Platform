import React, { useLayoutEffect, useMemo, useState } from "react";
import { Button, Table, Modal } from "../components";
import { useNavigate } from "react-router-dom";
import { useStateContext } from "../contexts/ContextProvider";
import axios from "axios";
// import { BsFillTrashFill } from "react-icons/bs"
// import { BsSearch } from "react-icons/bs"

const Deploy = () => {
    const { mainColor, disabledColor, base_url, isModalOpen, setIsModalOpen, checkedInputs, setCheckedInputs } = useStateContext();
    const [deploys, setDeploys] = useState([]);
    // const [stackData, setStackData] = useState();
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
                setDeploys(response.data);
            })
            .catch((error) => {
                console.log("error", error);
            })
    }

    // const deleteStack = (stack_name) => {
    //     axios({
    //         method: "DELETE",
    //         url: `${base_url}/api/v1/stacks/${stack_name}`,
    //         headers: {
    //             "Authorization": localStorage.getItem("accessToken")
    //         },
    //     })
    //         .then((resp) => {
    //             console.log("resp", resp)
    //             alert("선택한 스택을 삭제하였습니다.")
    //             // getStackList();
    //         })
    //         .catch((error) => {
    //             console.log(error)
    //         })
    // }

    const columns = [
        {
            accessor: "stack_id",
            Header: "ID",
        },
        {
            accessor: "stack_name",
            Header: "스택명"
        },
        {
            accessor: "description",
            Header: "설명"
        },
        {
            accessor: "csp_type",
            Header: "CSP 타입"
        },
        {
            accessor: "stack_type",
            Header: "스택 타입"
        },
        {
            accessor: "created_at",
            Header: "생성 날짜"
        },
        // {
        //     accessor: "delete",
        //     Header: "삭제",
        //     Cell: tableProps => (
        //         <div className="flex items-center justify-center">
        //             <button onClick={() => {
        //                 if (window.confirm("선택한 스택을 삭제하시겠습니까?")) {
        //                     deleteStack(tableProps.data[tableProps.row.index].stack_name)
        //                 }
        //             }} style={{ color: "black", }}>
        //                 <BsFillTrashFill />
        //             </button>
        //         </div>
        //     ),
        //     minWidth: 140,
        //     width: 200,
        // },
        // {
        //     accessor: "parameters",
        //     Header: "변수 확인",
        //     Cell: tableProps => (
        //         <div className="flex items-center justify-center">
        //             <button onClick={() => {
        //                 setStackData(tableProps.data[tableProps.row.index]);
        //                 setIsModalOpen(true);
        //             }} style={{ color: "black", }}>
        //                 <BsSearch />
        //             </button>
        //         </div>
        //     ),
        //     minWidth: 140,
        //     width: 200,
        // },
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
        </>
    );
};

export default Deploy;