import React, { useLayoutEffect, useMemo, useState, useEffect } from "react";
import { useStateContext } from "../contexts/ContextProvider";
import axios from "axios";
import { redirect, useNavigate } from "react-router-dom";
import { Table, Button, Modal } from "../components";
import { MdOutlineCancel } from "react-icons/md";
import { BsFillTrashFill } from "react-icons/bs"


const refresh = () => {
    window.location.replace("/user");
}

const ModalComponentCreateProvider = ({ team }) => {
    const { setIsModalOpen, mainColor, base_url } = useStateContext();
    const [roles, setRoles] = useState([]);

    const changeHandler = (checked, role) => {
        if (checked) {
            setRoles([...roles, role])
        }
        else {
            setRoles(roles.filter((el) => el !== role))
        }
    }

    const createUser = () => {
        const user_username = document.getElementById("user_username").value;
        const user_fullname = document.getElementById("user_fullname").value;
        const user_password = document.getElementById("user_password").value;
        const user_email = document.getElementById("user_email").value;

        if (user_username && user_fullname && user_password && user_email) {
            axios({
                method: "POST",
                url: `${base_url}/api/v1/user`,
                headers: {
                    "Authorization": localStorage.getItem("accessToken")
                },
                data: {
                    username: user_username,
                    fullname: user_fullname,
                    password: user_password,
                    email: user_email,
                    role: roles,
                    is_active: true,
                    team: team,
                }
            })
                .then((response) => {
                    console.log(response);
                    alert("유저 계정이 생성되었습니다.");
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
                        <p className="mb-1">Username</p>
                        <input id="user_username" type="text" className="border-2 p-2 rounded-xl w-full" />
                    </div>
                    <div>
                        <p className="mb-1">Full name</p>
                        <input id="user_fullname" type="text" className="border-2 p-2 rounded-xl w-full" />
                    </div>
                    <div>
                        <p className="mb-1">Password</p>
                        <input id="user_password" type="text" className="border-2 p-2 rounded-xl w-full" />
                    </div>
                    <div>
                        <p className="mb-1">e-mail</p>
                        <input id="user_email" type="text" className="border-2 p-2 rounded-xl w-full" />
                    </div>
                    <div>
                        <p className="mb-1">Role</p>
                        {/* <input id="provider_profile" type="text" className="border-2 p-2 rounded-xl w-full" /> */}
                        <div>
                            <input type="checkbox" id="system_manager" value="system_manager" onChange={(e) => {
                                changeHandler(e.target.checked, e.target.value)
                            }} checked={roles.includes("system_manager") ? true : false} />
                            <label htmlFor="system_manager">&nbsp;system manager</label>
                        </div>
                        <div>
                            <input type="checkbox" id="user" value="user" onChange={(e) => {
                                changeHandler(e.target.checked, e.target.value)
                            }} checked={roles.includes("user") ? true : false} />
                            <label htmlFor="user">&nbsp;user</label>
                        </div>
                        <div>
                            <input type="checkbox" id="team_manager" value="team_manager" onChange={(e) => {
                                changeHandler(e.target.checked, e.target.value)
                            }} checked={roles.includes("team_manager") ? true : false} />
                            <label htmlFor="team_manager">&nbsp;team manager</label>
                        </div>
                    </div>
                </div>
                <div className="mt-10">
                    <Button
                        color="white"
                        bgColor={mainColor}
                        text="새 사용자 생성"
                        borderRadius="10px"
                        onClickFunc={() => {
                            if (window.confirm("사용자 계정을 생성하시겠습니까?")) {
                                createUser();
                            }
                        }}
                    />
                </div>
            </div>
        </>
    )
}

const User = () => {
    const { mainColor, base_url, isModalOpen, setIsModalOpen } = useStateContext();
    const [users, setUsers] = useState([]);
    const [team, setTeam] = useState("");

    const getUserList = () => {
        axios({
            method: 'GET',
            url: `${base_url}/api/v1/user`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then((response) => {
                console.log(response.data);
                setUsers(response.data);
            })
            .catch((error) => {
                console.log("error", error);
            })
    }

    const getMyInfo = () => {
        axios({
            method: "GET",
            url: `${base_url}/api/v1/user/${localStorage.getItem("username")}`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then((resp) => {
                // console.log(resp)
                setTeam(resp.data.team);
            })
            .catch((error) => {
                console.log(error)
            })
    }

    const columns = [
        {
            accessor: "id",
            Header: "ID",
        },
        {
            accessor: "username",
            Header: "이름"
        },
        {
            accessor: "fullname",
            Header: "Full Name"
        },
        {
            accessor: "email",
            Header: "e-mail"
        },
        {
            accessor: "role",
            Header: "권한",
            Cell: tableProps => (
                tableProps.data[tableProps.row.index].role.map((r, idx) => (
                    <span key={idx} className={`px-3 py-1 uppercase font-bold text-xs rounded-full shadow-sm 
                    ${r === 'system_manager' ? `bg-green-100 text-green-800`
                            : r === 'user' ? `bg-yellow-100 text-yellow-800` : `bg-red-100 text-red-800`}`}>
                        {r}
                    </span>
                ))
            )
        },
        {
            accessor: "created_at",
            Header: "생성 날짜"
        },
    ];

    useLayoutEffect(() => {
        getUserList();
        getMyInfo();
    }, []);

    return (
        <>
            <div className="px-10 py-5">
                <div className="flex justify-between p-3 m-3 border-b-2">
                    <div className="flex justfiy-center items-center text-2xl">'{team}' 팀에 속한 사용자 목록</div>
                    <Button
                        color="white"
                        bgColor={mainColor}
                        text="새 사용자 생성"
                        borderRadius="10px"
                        onClickFunc={() => {
                            setIsModalOpen(!isModalOpen);
                        }}
                    />
                </div>

                <Table columns={columns} data={users} />
            </div>

            {isModalOpen && <Modal title={"새 사용자 생성"}><ModalComponentCreateProvider team={team} /></Modal>}
        </>
    );
};

export default User;