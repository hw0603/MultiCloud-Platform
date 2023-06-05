import axios from "axios";
import React, { useEffect, useState } from "react";
import { useStateContext } from "../contexts/ContextProvider";
import { AiFillDatabase, AiTwotoneCloud } from "react-icons/ai";
import { TbPackageExport } from 'react-icons/tb';


const IframeEmbed = (link) => {
    return <iframe
        className="w-full h-full"
        src={`http://localhost:3001${link.link}&theme=light`}></iframe>
}

const Dashboard = () => {
    const { base_url, mainColor } = useStateContext();
    const [status, setStatus] = useState({});
    const [onlineStatus, setOnlineStatus] = useState({});
    const [instance, setInstance] = useState([]);
    const [isContentReady, setIsContentReady] = useState(null);
    const [panelIds, setPanelIds] = useState(null);

    const inst = "i-03deab673045bef9b";

    const getStatus = () => {
        axios({
            method: 'GET',
            url: `${base_url}/api/v1/`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then(resp => {
                // console.log(resp);
                setOnlineStatus(resp.data);
            })
    }

    const getCount = () => {
        axios({
            method: 'GET',
            url: `${base_url}/api/v1/status`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then(resp => {
                // console.log(resp);
                setStatus(resp.data);
            })
    }

    const getInstance = () => {
        // console.log("getInstance");
        axios({
            method: 'GET',
            url: `${base_url}/api/v1/instance/list`,
            headers: {
                "Authorization": localStorage.getItem("accessToken")
            },
        })
            .then(resp => {
                console.log("getInstance", resp.data.data);
                setInstance(resp.data.data);
                
                // console.log(instance);
            })
    }

    const getInstanceById = (id) => {
        console.log("getInstancebyId");
        setIsContentReady(false);

        if (id !== "") {
            axios({
                method: 'GET',
                url: `${base_url}/api/v1/instance/${id}?metrics=EBSWriteBytes&metrics=CPUUtilization&metrics=NetworkOut`,
                headers: {
                    "Authorization": localStorage.getItem("accessToken")
                },
            })
                .then(resp => {
                    console.log("resp", resp);
                    console.log(resp.data.data.panel_urls);
                    localStorage.setItem("panelId", JSON.stringify(resp.data.data.panel_urls));
                    setPanelIds(resp.data.data.panel_urls);
                    setIsContentReady(true);
                })
        }
    }

    useEffect(() => {
        getStatus();
        getCount();
        getInstance();
        if (localStorage.getItem("panelId")) {
            console.log("cached");
            // getInstanceById(localStorage.getItem("instanceId"));
            setPanelIds(JSON.parse(localStorage.getItem("panelId")));
        }
    }, []);

    const monitoringDiv = "bg-white border-2 rounded-xl w-160 flex-1 p-4 flex justify-between"
    return (
        <>
            <div className="flex flex-col p-6 gap-6 h-full">
                {/* 상단바 */}
                <div className="flex gap-6 h-1/5 justify-between">
                    <div className={monitoringDiv}>
                        <div>
                            <div className="font-bold text-lg mb-3">프로바이더</div>
                            <div className="text-3xl flex flex-1 items-center">{status.aws_count + status.azure_count + status.gcp_count}개</div>
                        </div>
                        <div className="flex items-center">
                            <div className="rounded-full p-2 text-6xl" style={{ color: `${mainColor}` }}>
                                <AiTwotoneCloud />
                            </div>
                        </div>
                    </div>
                    <div className={monitoringDiv}>
                        {/* <div className="font-bold text-lg mb-3">스택</div>
                        <div className="text-3xl flex flex-1 items-center">{status.stack_count}개</div> */}
                        <div>
                            <div className="font-bold text-lg mb-3">스택</div>
                            <div className="text-3xl flex flex-1 items-center">{status.stack_count}개</div>
                        </div>
                        <div className="flex items-center">
                            <div className="rounded-full p-2 text-6xl">
                                <AiFillDatabase />
                            </div>
                        </div>
                    </div>
                    <div className={monitoringDiv}>
                        {/* <div className="font-bold text-lg mb-3">배포</div>
                        <div className="text-3xl flex flex-1 items-center">{status.deploy_count}개</div> */}
                        <div>
                            <div className="font-bold text-lg mb-3">배포</div>
                            <div className="text-3xl flex flex-1 items-center">{status.deploy_count}개</div>
                        </div>
                        <div className="flex items-center">
                            <div className="rounded-full p-2 text-6xl">
                                <TbPackageExport />
                            </div>
                        </div>
                    </div>
                    <div className="bg-white border-2 rounded-xl w-160 flex-1 p-4">
                        <div className="font-bold text-lg mb-3">
                            시스템 연결 상태
                        </div>
                        <div className="flex gap-1 flex-wrap justify-center items-center">
                            {Object.entries(onlineStatus).map((item, idx) => (
                                <div key={idx} className="flex">
                                    <div className={item[1] ? "p-1 text-sm rounded-full bg-green-100 text-green-800" : "p-1 text-xs rounded-full bg-red-100 text-red-800"}>{item[0]}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
                {/* 상단바 */}

                {/* 대시보드 */}
                <div className="flex gap-6 flex-1">
                    <div className="bg-white border-2 rounded-xl w-3/5 p-4 flex-col flex">
                        <div className="flex justify-between items-center">
                            <div className="font-bold text-lg">
                                CPU Utilization
                            </div>
                            <div>
                                <select id="stack_selectbox" className="border-2 p-1 rounded-xl" defaultValue="" onChange={(e) => {
                                    if (e.target.value !== "") {
                                        getInstanceById(e.target.value);
                                        localStorage.setItem("instanceId", e.target.value);
                                    }
                                }}>
                                    <option value="">인스턴스 선택</option>
                                    {instance.map((i, idx) => (
                                        <option key={idx} id={i} >{i}</option>
                                    ))}

                                </select>
                            </div>
                        </div>
                        <div className="flex flex-1 mt-4 rounded-xl justify-center items-center">
                            <div className="w-full h-full flex justify-center items-center">
                                {panelIds ? <IframeEmbed link={panelIds.cpu} /> : <span>인스턴스를 선택하세요</span>}
                            </div>
                        </div>
                    </div>

                    <div className="flex-1 gap-4 flex flex-col">
                        <div className="bg-white rounded-xl border-2 h-1/2 p-4 flex-col flex">
                            <div className="font-bold text-lg">
                                Network In
                            </div>
                            <div className="flex flex-1 rounded-xl mt-2 justify-center items-center">
                                <div className="w-full h-full flex justify-center items-center">
                                    {panelIds ? <IframeEmbed link={panelIds.ebs} /> : <span>인스턴스를 선택하세요</span>}
                                </div>
                            </div>
                        </div>

                        <div className="bg-white rounded-xl border-2 h-1/2 p-4 flex-col flex">
                            <div className="font-bold text-lg">
                                EBSWriteBytes
                            </div>
                            <div className="flex flex-1 rounded-xl mt-2 justify-center items-center">
                                <div className="w-full h-full flex justify-center items-center">
                                    {panelIds ? <IframeEmbed link={panelIds.network} /> : <span>인스턴스를 선택하세요</span>}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                {/* 대시보드 */}
            </div>
        </>
    );
};

export default Dashboard;