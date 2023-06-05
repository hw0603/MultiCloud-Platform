import React, { useLayoutEffect, useState } from "react";
import { MdOutlineCancel } from "react-icons/md";
import { useNavigate } from "react-router-dom";
import { Button } from ".";
import { useStateContext } from "../contexts/ContextProvider";
import profilePic from "../data/profilePic.png";
import axios from "axios";

const UserProfile = () => {
  const navigate = useNavigate();
  const { mainColor, initialState, setIsClicked, setIsAuthorized, base_url } = useStateContext();
  const roles = localStorage.getItem("role").split(',');
  const [email, setEmail] = useState("");
  const getEmail = () => {
    axios({
      method: "GET",
      url: `${base_url}/api/v1/user/${localStorage.getItem("username")}`,
      headers: {
          "Authorization": localStorage.getItem("accessToken")
      },
    })
      .then((resp) => {
        setEmail(resp.data.email);
      })
      .catch((e) => {
        console.log("error", e)
      })
  }

  useLayoutEffect(() => {
    getEmail();
  } ,[])

  return (
    <div className="nav-item absolute right-1 top-16 bg-white dark:bg-[#42464D] p-8 rounded-lg w-96 border-1">
      <div className="flex justify-between items-center">
        <p className="font-semibold text-lg dark:text-gray-200">유저 프로필</p>
        <Button
          icon={<MdOutlineCancel />}
          color="rgb(153, 171, 180)"
          bgHoverColor="light-gray"
          size="2xl"
          borderRadius="50%"
          onClickFunc={() => setIsClicked(initialState)}
        />
      </div>
      <div className="flex gap-5 items-center mt-6 border-color border-b-2 pb-6">
        <img
          className="rounded-full h-24 w-24"
          src={profilePic}
          alt="user-profile"
        />
        <div>
          <p className="font-semibold text-xl dark:text-gray-200">
            {localStorage.getItem("username")}
          </p>
          <p className="text-gray-500 text-sm py-2 flex gap-2 dark:text-gray-400">
            {
              roles.map((r, idx) => (
                <span key={idx} className={`px-3 py-1 uppercase font-bold text-xs rounded-full shadow-sm 
                ${r === 'system_manager' ? `bg-green-100 text-green-800`
                        : r === 'user' ? `bg-yellow-100 text-yellow-800` : `bg-red-100 text-red-800`}`}>
                    {r}
                </span>
              ))
            }
          </p>
          <p className="text-gray-500 text-sm font-semibold dark:text-gray-400">
            {email}
          </p>
        </div>
      </div>
      <div className="mt-5">
        <Button
          color="white"
          bgColor={mainColor}
          text="로그아웃"
          borderRadius="10px"
          width="full"
          onClickFunc={() => {
            setIsAuthorized(false);
            localStorage.clear();
            setIsClicked(initialState);
            navigate("/login");
          }}
        />
      </div>
    </div>
  );
};

export default UserProfile;
