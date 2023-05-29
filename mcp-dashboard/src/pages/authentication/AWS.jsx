import React, { useLayoutEffect, useMemo, useState } from "react";
import Button from "../../components/Button";
import { useStateContext } from "../../contexts/ContextProvider";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Table } from "../../components";

const AWS = () => {
    const { mainColor, base_url, stacks, setStacks, isAuthorized } = useStateContext();
    const navigate = useNavigate();
    const [providers, setProviders] = useState([]);
    // const providers = [];

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
        console.log("useLayoutEffect")
        console.log(providers)
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
                            navigate('/provider/new');
                        }}
                    />
                </div>

                <Table columns={columns} data={providers} />
            </div>
        </>
    );
};

export default AWS;