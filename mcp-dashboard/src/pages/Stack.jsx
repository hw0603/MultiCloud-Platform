import React, { useLayoutEffect, useMemo, useState } from "react";
import { Button, Table, Modal } from "../components";
import { useNavigate } from "react-router-dom";
import { useStateContext } from "../contexts/ContextProvider";
import axios from "axios";
import { BsFillTrashFill } from "react-icons/bs"
import { BsSearch } from "react-icons/bs"

let ModalContentType = -1;
let stackIdx = -1;

const refresh = () => {
    window.location.replace("/stack");
}

const ObjCompare = (obj1, obj2) => {
    const Obj1_keys = Object.keys(obj1);
    const Obj2_keys = Object.keys(obj2);
    if (Obj1_keys.length !== Obj2_keys.length) {
        return false;
    }
    for (let k of Obj1_keys) {
        if (obj1[k] !== obj2[k]) {
            return false;
        }
    }
    return true;
}

const ModalComponentCreateStack = () => {
    const { mainColor, base_url } = useStateContext();

    const createStack = () => {
        const stackType = document.getElementById("stackType").value;
        const CSPType = document.getElementById("CSPType").value;
        const stackName = document.getElementById("stackName").value;
        const stackDesc = document.getElementById("stackDesc").value;

        if (stackType && CSPType && stackName && stackDesc) {
            axios({
                method: "POST",
                url: `${base_url}/api/v1/stacks`,
                headers: {
                    "Authorization": localStorage.getItem("accessToken")
                },
                data: {
                    stack_name: stackName,
                    stack_type: stackType,
                    csp_type: CSPType,
                    description: stackDesc,
                }
            })
                .then((resp) => {
                    console.log(resp)
                    alert("스택이 생성되었습니다.")
                    refresh();
                })
                .catch((error) => {
                    console.log("error", error)
                })
        }
    }

    return (
        <div>
            <div className="mt-6 flex flex-col gap-4">
                <div>
                    <select id="stackType" className="border-2 p-3 rounded-xl w-full" defaultValue="">
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
                </div>
                <div>
                    <select id="CSPType" className="border-2 p-3 rounded-xl w-full" defaultValue="">
                        <option value="">CSP 종류 선택</option>
                        <option value="aws">AWS</option>
                        <option value="gcp">GCP</option>
                        <option value="azure">Azure</option>
                        <option value="custom">Custom</option>
                    </select>
                </div>
                <div>
                    <p className="mb-1">Stack Name</p>
                    <input id="stackName" type="text" className="border-2 p-2 rounded-xl w-full" />
                </div>
                <div>
                    <p className="mb-1">Description</p>
                    <input id="stackDesc" type="text" className="border-2 p-2 rounded-xl w-full" />
                </div>
            </div>
            <div className="mt-10">
                <Button
                    color="white"
                    bgColor={mainColor}
                    text="새 스택 생성"
                    borderRadius="10px"
                    onClickFunc={() => {
                        if (window.confirm("스택을 생성하시겠습니까?")) {
                            createStack();
                        }
                    }}
                />
            </div>
        </div>
    );
};

const ModalComponentStackParameter = ({ stackData }) => {
    const variables = Object.entries(stackData.var_json.variable);
    return (
        <>
            <div className="flex flex-wrap gap-4 mt-4">
                {variables.map((item) => (
                    <div key={item[0]} className="border-2 w-2/5 rounded-xl p-2 flex-auto">
                        <span className="font-bold text-lg">{item[0]}</span><span className="text-sm">{` <${item[1].type}>`}</span>
                        <h2 className="text-sm">{`기본값 : ${item[1].default} `}</h2>
                    </div>
                ))}
            </div>
        </>
    );
}

const Stack = () => {
    const { mainColor, base_url, isModalOpen, setIsModalOpen, checkedInputs, setCheckedInputs } = useStateContext();
    const [stacks, setStacks] = useState([]);
    const [stackData, setStackData] = useState();
    const navigate = useNavigate();

    const changeHandler = (checked, item) => {
        if (checked) {
            setCheckedInputs([...checkedInputs, item]);
        }
        else {
            setCheckedInputs(checkedInputs.filter(el => ObjCompare(el, item) === false));
        }
    }

    const getStackList = () => {
        axios({
            method: 'GET',
            url: `${base_url}/api/v1/stacks`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then((response) => {
                setStacks(response.data);
            })
            .catch((error) => {
                console.log("error", error);
            })
    }

    const deleteStack = (stack_name) => {
        axios({
            method: "DELETE",
            url: `${base_url}/api/v1/stacks/${stack_name}`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then((resp) => {
                console.log("resp", resp)
                alert("선택한 스택을 삭제하였습니다.")
                getStackList();
            })
            .catch((error) => {
                console.log(error)
            })
    }

    const columns = [
        {
            accessor: "select",
            Header: "",
            Cell: (tableProps) => (
                <div className="flex items-center justify-center">
                    <input type="checkbox" onChange={(e) => {
                        changeHandler(e.target.checked, tableProps.data[tableProps.row.index])
                    }}
                        checked={checkedInputs.includes(tableProps.data[tableProps.row.index]) ? true : false}
                    />
                </div>
            ),
            minWidth: 10,
            width: 10,
        },
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
                            deleteStack(tableProps.data[tableProps.row.index].stack_name)
                        }
                    }} style={{ color: "black", }}>
                        <BsFillTrashFill />
                    </button>
                </div>
            ),
            minWidth: 140,
            width: 200,
        },
        {
            accessor: "parameters",
            Header: "변수 확인",
            Cell: tableProps => (
                <div className="flex items-center justify-center">
                    <button onClick={() => {
                        ModalContentType = 3;
                        setStackData(tableProps.data[tableProps.row.index]);
                        setIsModalOpen(true);
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
                                    ModalContentType = 1;
                                    setIsModalOpen(!isModalOpen);
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
                                    // ModalContentType = 2;
                                    // setIsModalOpen(!isModalOpen);
                                    // console.log(checkedInputs)
                                    // window.location.replace("/deploy/new");
                                    navigate("/deploy/new", {
                                        state: {
                                            checkedInputs: checkedInputs
                                        }
                                    })
                                }}
                            />
                        </div>
                    </div>
                </div>

                <Table columns={columns} data={stacks} />
            </div>
            {isModalOpen &&
                (ModalContentType == 1 ? <Modal title="새 스택 생성"><ModalComponentCreateStack /></Modal> :
                    ModalContentType == 2 ? <Modal title="dummy"></Modal> :
                        <Modal title="파라미터" width="3/5"><ModalComponentStackParameter stackData={stackData} /></Modal>
                )}
        </>
    );
};

export default Stack;