import React, { useLayoutEffect, useMemo, useState, useEffect } from "react";
import { useStateContext } from "../contexts/ContextProvider";
import axios from "axios";
import { Table } from "../components";
// import "../components/Modal.css";
// import { MdOutlineCancel } from "react-icons/md";
// import { BsFillTrashFill } from "react-icons/bs"

const Log = () => {
    const { base_url, username } = useStateContext();
    const [logs, setLogs] = useState([]);

    const getLog = () => {
        axios({
            method: 'GET',
            url: `${base_url}/api/v1/activity_log/id/${username}`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then((response) => {
                setLogs(response.data);
            })
            .catch((error) => {
                console.log("error", error);
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
                accessor: "username",
                Header: "사용자명"
            },
            {
                accessor: "action",
                Header: "내용"
            },
            {
                accessor: "created_at",
                Header: "시간"
            },
        ], []
    );

    useLayoutEffect(() => {
        getLog();
    }, []);

    return (
        <>
            <div className="px-10 py-5">
                <div className="flex justify-between p-3 m-3 border-b-2">
                    <div className="flex justfiy-center items-center text-2xl">활동 로그 </div>
                </div>

                
                <Table columns={columns} data={logs} />

            </div>

            {/* {isModalOpen && <Modal />} */}
        </>
    );
};

export default Log;