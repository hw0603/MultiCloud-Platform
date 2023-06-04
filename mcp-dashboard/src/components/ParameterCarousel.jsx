import React, { useEffect, useState, useRef, useLayoutEffect } from "react";
import "./Carousel.css";
import { MdKeyboardArrowLeft, MdKeyboardArrowRight } from "react-icons/md"
import { Button } from "./";
import { useStateContext } from "../contexts/ContextProvider";

const ParameterCarousel = ({ deployDetails }) => {
    const { mainColor, parameters, setParameters, deployDetail, setDeployDetail } = useStateContext();
    const [current, setCurrent] = useState(0);
    const [style, setStyle] = useState({
        marginLeft: `-${current}00%`
    });

    const activeIdx = "bg-gray-500 rounded-full w-3 h-3";
    const normalIdx = "bg-gray-300 rounded-full w-3 h-3";

    const moveSlide = (i) => {
        setCurrent(Math.abs(current + i) % deployDetails.length);
    };

    useEffect(() => {
        console.log(deployDetails);
    }, []);

    useEffect(() => {
        setStyle({ marginLeft: `-${current}00%` });
    }, [current]);

    return (
        <>
            <div className="flex items-center">
                <div className="flex flex-col justify-between">
                    <div className="flex gap-4 mb-2">
                        <div className="flex items-center cursor-pointer text-2xl text-gray-600 border-1 p-2 rounded-full mr-2 bg-white" onClick={() => {
                            if (current !== 0) {
                                moveSlide(-1);
                            }
                        }}>
                            <MdKeyboardArrowLeft />
                        </div>

                        <div className="flex gap-4 justify-center items-center flex-1">
                            {deployDetails.map((x, i) => {
                                return (
                                    <div
                                        key={i}
                                        className={i === current ? `${activeIdx}` : `${normalIdx}`}
                                    >
                                    </div>
                                )
                            })}
                        </div>

                        <div className="flex items-center cursor-pointer text-2xl text-gray-600 border-1 p-2 rounded-full mr-2 bg-white" onClick={() => {
                            if (current != deployDetails.length - 1) {
                                moveSlide(1);
                            }
                        }}>
                            <MdKeyboardArrowRight />
                        </div>
                    </div>

                    <div>


                        <div className="w-500 overflow-hidden">
                            <div className="flex items-start" style={style}>
                                {deployDetails.map((detail, i) => {
                                    return (
                                        <div key={i} className="w-500 flex-none bg-white border-2 rounded-2xl p-6">
                                            <div className="font-bold text-2xl">
                                                {detail.stack_name}
                                            </div>
                                            <div className="gap-2 flex-col mt-4 flex">
                                                {
                                                    Object.entries(detail.variables).map((item, idx) => (
                                                        <div key={idx} className="pb-4 pt-1 border-t-2 flex flex-col gap-2">
                                                            <div className="mb-1 font-bold text-lg">{item[0]}</div>
                                                            <div className="text-sm">{item[1]}</div>
                                                        </div>
                                                    ))
                                                }
                                            </div>
                                        </div>
                                    )
                                })}
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </>
    );
}

export default ParameterCarousel;