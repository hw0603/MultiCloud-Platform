import React, { useLayoutEffect } from "react";
import Button from "../components/Button";
import { useStateContext } from "../contexts/ContextProvider";
import axios from "axios";
import { useNavigate } from "react-router-dom";



const Stack = () => {
    const { mainColor, base_url, stacks, setStacks } = useStateContext();
    const navigate = useNavigate();
    useLayoutEffect(() => {
        console.log("useLayoutEffect");
        axios.get(`${base_url}/api/v1/stacks`)
            .then((response) => {
                setStacks(response.data);
            })
            .catch((error) => {
                console.log(error);
            })
            .finally(() => {
                console.log("stacks", stacks);
            })
    }, []);

    return (
        <>
            <div className="p-10">
                <div className="flex justify-between p-3 m-3 border-b-2">
                    <div className="flex justfiy-center items-center text-2xl">관리 중인 스택</div>
                    <Button
                        color="white"
                        bgColor={mainColor}
                        text="새 스택 생성"
                        borderRadius="10px"
                        onClick = {() => {
                            navigate('/stack/new');
                        }}
                    />
                </div>

                <div>
                    <div className="flex justify-between items-center gap-5 px-5">
                        <span className="flex items-center gap-4 ml-1">
                            <p>ID</p>
                            <p>스택명</p>
                        </span>
                        <div className="flex gap-5">
                            <p>타입</p>
                            <p className="ml-10 mr-6">생성 일자</p>
                        </div>
                    </div>
                </div>

                <div className="p-3">
                    {stacks.map((stack) => (
                        <div key={stack.stack_id} className="flex justify-between items-center mb-4 bg-white border-1 rounded-2xl p-4 gap-7">
                            <div className="flex items-center gap-5">
                                <p>{stack.stack_id}</p>
                                <div className="flex gap-4">
                                    <div>
                                        <p className="text-xl font-semibold">{stack.stack_name}</p>
                                        <p className="text-sm text-gray-400">{stack.description}</p>
                                    </div>
                                </div>
                            </div>
                            <div className="flex">
                                <p>{stack.stack_type}</p>
                                <div className="ml-16">
                                    <p className="text-sm text-gray-400">{stack.created_at.substr(0, 10)}</p>
                                    <p className="text-sm text-gray-400">{stack.created_at.substr(-8)}</p>
                                </div>
                            </div>
                            {/* <p>{stack.created_at}</p> */}
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
};

export default Stack;