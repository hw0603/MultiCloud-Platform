import React, { useEffect, useState, useRef, useLayoutEffect } from "react";
import "./Carousel.css";
import { MdKeyboardArrowLeft, MdKeyboardArrowRight } from "react-icons/md"
import { Button } from "./";
import { useStateContext } from "../contexts/ContextProvider";

const Carousel = ({ stacks }) => {
    // console.log(JSON.parse(JSON.stringify(stacks[0].var_json.variable)));
    const arr = [1, 2, 3, 4, 5, 6];
    const { mainColor, parameters, setParameters, deployDetail, setDeployDetail } = useStateContext();
    const [current, setCurrent] = useState(0);
    const [style, setStyle] = useState({
        marginLeft: `-${current}00%`
    });

    // let parameters = {};
    let confirmed = [];

    const activeIdx = "text-xl font-bold bg-yellow-100 text-yellow-800 rounded-full p-2";
    const prevIdx = "text-lg bg-green-100 text-green-800 rounded-full p-2";
    const normalIdx = "text-lg";

    const saveParameter = (idx) => {
        let varList = stacks[idx].var_list;
        let thisstack = stacks[idx];
        // console.log("thisstack", thisstack);
        const stackName = stacks[idx].stack_name;
        let t = {};
        for (let i = 0; i < varList.length; i++) {
            let varName = varList[i];
            // console.log(varName, "input 값 :", document.getElementById(`${thisstack.stack_name}_${varName}`).value);
            if (document.getElementById(`${thisstack.stack_name}_${varName}`).value) {
                t[varName] = document.getElementById(`${thisstack.stack_name}_${varName}`).value;
            }
            else {
                if (thisstack.var_json.variable[varName].default !== undefined) {
                    t[varName] = stacks[idx].var_json.variable[varName].default;
                }
                else {
                    t[varName] = "";
                }
            }
        }
        // console.log("t", t);
        // parameters[stackName] = t;
        // console.log("deployDetail", deployDetail);
        for (let i = 0; i < deployDetail.length; i++) {
            // let t = deployDetail[i];
            if (deployDetail[i].stack_name === stackName) {
                deployDetail[i].variables = t;
            }
        }
        // console.log("deployDetail", deployDetail);
    }

    const moveSlide = (i) => {
        saveParameter(current);
        setCurrent(Math.abs(current + i) % stacks.length);
    };

    useEffect(() => {
        setStyle({ marginLeft: `-${current}00%` });
    }, [current]);

    useEffect(() => {
        for (let i = 0; i < stacks.length; i++) {
            let t = {};
            confirmed.push(false);
            parameters[stacks[i].stack_name] = {};
            t["stack_name"] = stacks[i].stack_name;
            t["tfvar_file"] = "terraform.tfvars";
            t["variables"] = {};
            deployDetail.push(t);
        }
    }, []);

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
                            {stacks.map((x, i) => {
                                return (
                                    <div
                                        key={i}
                                        className={(
                                            i < current ? `${prevIdx}` : (
                                                i === current ? `${activeIdx}` : `${normalIdx}`
                                            )
                                        )}
                                    >
                                        {x.stack_type}
                                    </div>
                                )
                            })}
                        </div>

                        <div className="flex items-center cursor-pointer text-2xl text-gray-600 border-1 p-2 rounded-full mr-2 bg-white" onClick={() => {
                            if (current != stacks.length - 1) {
                                moveSlide(1);
                            }
                        }}>
                            <MdKeyboardArrowRight />
                        </div>
                    </div>

                    <div>


                        <div className="w-500 overflow-hidden">
                            <div className="flex items-start" style={style}>
                                {stacks.map((stack, i) => {
                                    return (
                                        <div key={i} className="w-500 flex-none bg-white border-2 rounded-2xl p-6">
                                            <div className="font-bold text-2xl">
                                                {stack.stack_name}
                                            </div>
                                            <div className="gap-2 flex-col mt-4 flex">
                                                {
                                                    Object.entries(stack.var_json.variable).map((item, idx) => (
                                                        // console.log(idx, item)
                                                        <div key={idx} className="pb-4 pt-1 border-t-2 flex flex-col gap-2">
                                                            <div className="mb-1">{item[0]}</div>
                                                            {item[1].description && <div className="text-xs text-slate-400">{item[1].description}</div>}
                                                            <input type="text" name="" id={`${stack.stack_name}_${item[0]}`} placeholder={item[1].default ? item[1].default.toString() : ""} className="border-2 rounded-xl p-1 w-80"
                                                            />
                                                        </div>
                                                    ))
                                                }
                                                <div className="flex justify-between">
                                                    <div></div>
                                                    <Button
                                                        color="white"
                                                        bgColor={mainColor}
                                                        text="완료"
                                                        borderRadius="10px"
                                                        onClickFunc={() => {
                                                            saveParameter(current);
                                                            console.log(deployDetail);
                                                        }}
                                                    />
                                                </div>
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

export default Carousel;