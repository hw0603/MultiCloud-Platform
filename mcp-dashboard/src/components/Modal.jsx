import React from "react";
import { useStateContext } from "../contexts/ContextProvider";
import {MdOutlineCancel} from "react-icons/md"
import {Button} from ".";

const Modal = ({ children, title }) => {
    const { setIsModalOpen, mainColor, base_url } = useStateContext();
    const closeModal = () => {
        setIsModalOpen(false);
    }

    return (
        <div className="absolute left-0 top-0 min-w-full min-h-full bg-black/50 flex justify-center items-center" id="modal_mask" onClick={closeModal}>
            <div className="m-10 bg-white w-1/3 p-10 rounded-2xl" onClick={(event) => {
                event.stopPropagation();
            }
            }>
                <div className="flex justify-between items-center">
                    <h1 className="font-bold text-xl">{title}</h1>
                    <Button
                        icon={<MdOutlineCancel />}
                        color="rgb(153, 171, 180)"
                        bgHoverColor="light-gray"
                        size="2xl"
                        borderRadius="50%"
                        onClickFunc={closeModal}
                    />
                </div>
                {children}
            </div>
        </div>
    );
}

export default Modal;