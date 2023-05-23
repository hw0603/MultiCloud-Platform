import axios from "axios";
import React, { useEffect } from "react";
import { useStateContext } from "../contexts/ContextProvider";

const Home = () => {
    // const {base_url} = useStateContext();
    // useEffect(() => {
    //     // const axios = require('axios');
    //     axios.get(`${base_url}/api/v1/`)
    //         .then((response) => {
    //             console.log(response)
    //         })
    //         .catch((error) => {
    //             console.log(error)
    //         })
    // }, []);

    return (
        <>
            <div className="mt-12">
                <div>
                    {/* <h1 className="flex flex-wrap justify-start text-xl ml-20 mb-4">개요</h1> */}

                    <div className="flex flex-wrap justify-center">
                        <div className="bg-gray-200 m-3 p-4 rounded-2xl w-3/5 border-1">
                            <div className="flex justify-between gap-1">
                                <div className="bg-white m-3 p-4 rounded-2xl w-48 border-1">
                                    <div>
                                        <p className="text-l font-bold">관리 중인 스택</p>
                                        <p className="mt-3 text-2xl">4개</p>
                                    </div>
                                </div>
                                <div className="bg-white m-3 p-4 rounded-2xl w-48 border-1">
                                    <div>
                                        <p className="text-l font-bold">관리 중인 배포</p>
                                        <p className="mt-3 text-2xl">3개</p>
                                    </div>
                                </div>
                                <div className="bg-white m-3 p-4 rounded-2xl w-48 border-1">
                                    <div>
                                        <p className="text-l font-bold">관리 중인 태스크</p>
                                        <p className="mt-3 text-2xl">2개</p>
                                    </div>
                                </div>
                            </div>

                            <div className="flex justify-between gap-1">
                                <div className="bg-white m-3 p-4 rounded-2xl w-48 border-1">
                                    <div>
                                        <p className="text-l font-bold">관리 중인 스택</p>
                                        <p className="mt-3 text-2xl">4개</p>
                                    </div>
                                </div>
                                <div className="bg-white m-3 p-4 rounded-2xl w-48 border-1">
                                    <div>
                                        <p className="text-l font-bold">관리 중인 배포</p>
                                        <p className="mt-3 text-2xl">3개</p>
                                    </div>
                                </div>
                                <div className="bg-white m-3 p-4 rounded-2xl w-48 border-1">
                                    <div>
                                        <p className="text-l font-bold">관리 중인 태스크</p>
                                        <p className="mt-3 text-2xl">2개</p>
                                    </div>
                                </div>

                            </div>

                        </div>
                    </div>
                </div>


                <div>
                    <h1 className="flex flex-wrap justify-start text-xl ml-20 mb-4 mt-20">인스턴스 모니터링</h1>

                    <div className="flex flex-wrap gap-10 justify-center">
                        <div className="bg-white dark:text-gray-200 dark:bg-secondary-dark-bg m-3 p-4 rounded-2xl md:w-500 border-1">
                            <div className="flex">
                                <p className="font-semibold text-xl">예시 대시보드 1</p>
                            </div>
                            <div className="mt-10 mb-10 flex gap-10 flex-wrap justify-center">
                                <iframe src="http://localhost:3002/d-solo/rYdddlPWk/node-exporter-full?orgId=1&from=1683961028267&to=1683962828267&panelId=77" width="450" height="200" frameborder="0"></iframe>
                            </div>
                        </div>

                        <div className="bg-white dark:text-gray-200 dark:bg-secondary-dark-bg m-3 p-4 rounded-2xl md:w-500 border-1">
                            <div className="flex">
                                <p className="font-semibold text-xl">예시 대시보드 2</p>
                            </div>
                            <div className="mt-10 mb-10 flex gap-10 flex-wrap justify-center">
                                <iframe src="http://localhost:3002/d-solo/rYdddlPWk/node-exporter-full?orgId=1&from=1683961028267&to=1683962828267&panelId=77" width="450" height="200" frameborder="0"></iframe>
                            </div>
                        </div>
                    </div>

                    <div className="flex flex-wrap gap-10 justify-center">
                        <div className="bg-white dark:text-gray-200 dark:bg-secondary-dark-bg m-3 p-4 rounded-2xl md:w-500 border-1">
                            <div className="flex">
                                <p className="font-semibold text-xl">예시 대시보드 3</p>
                            </div>
                            <div className="mt-10 mb-10 flex gap-10 flex-wrap justify-center">
                                <iframe src="http://localhost:3002/d-solo/rYdddlPWk/node-exporter-full?orgId=1&from=1683961028267&to=1683962828267&panelId=77" width="450" height="200" frameborder="0"></iframe>
                            </div>
                        </div>

                        <div className="bg-white dark:text-gray-200 dark:bg-secondary-dark-bg m-3 p-4 rounded-2xl md:w-500 border-1">
                            <div className="flex">
                                <p className="font-semibold text-xl">예시 대시보드 4</p>
                            </div>
                            <div className="mt-10 mb-10 flex gap-10 flex-wrap justify-center">
                                <iframe src="http://localhost:3002/d-solo/rYdddlPWk/node-exporter-full?orgId=1&from=1683961028267&to=1683962828267&panelId=77" width="450" height="200" frameborder="0"></iframe>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Home;