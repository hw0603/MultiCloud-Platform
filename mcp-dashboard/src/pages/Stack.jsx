import React, { useLayoutEffect, useMemo, useState } from "react";
import { Button, Table } from "../components";
import { useStateContext } from "../contexts/ContextProvider";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { BsFillTrashFill } from "react-icons/bs"

const Stack = () => {
    const { mainColor, base_url } = useStateContext();
    const navigate = useNavigate();
    const [stacks, setStacks] = useState([]);

    const getStackList = () => {
        axios({
            method: 'GET',
            url: `${base_url}/api/v1/stacks`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then((response) => {
                console.log(response);
                setStacks(response.data);
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
                getStackList();
            })
            .catch((error) => {
                console.log(error)
            })
    }

    const columns = useMemo(
        () => [
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
            {
                accessor: "delete",
                Header: "삭제",
                Cell: tableProps => (
                    <div className="flex items-center justify-center">
                        <button onClick={() => {
                            if (window.confirm("선택한 스택을 삭제하시겠습니까?")) {
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
        getStackList();
    }, []);

    return (
        <>
            <div className="px-10 py-5">
                <div className="flex justify-between p-3 m-3 border-b-2">
                    <div className="flex justfiy-center items-center text-2xl">관리 중인 스택 목록</div>
                    <div className="gap-4 flex">
                        <div>
                            <Button
                                color="white"
                                bgColor={mainColor}
                                text="새 스택 생성"
                                borderRadius="10px"
                                onClickFunc={() => {
                                    // setIsModalOpen(!isModalOpen);
                                }}
                            />
                        </div>
                        <div>
                            <Button
                                color="white"
                                bgColor={mainColor}
                                text="새 배포 생성"
                                borderRadius="10px"
                                onClickFunc={() => {
                                    // setIsModalOpen(!isModalOpen);
                                }}
                            />
                        </div>
                    </div>
                </div>

                <Table columns={columns} data={stacks} />
            </div>
        </>
    );
};

export default Stack;