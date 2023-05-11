import React from "react";
import { MdOutlineCancel } from "react-icons/md";

import { Button } from ".";
// import { userProfileData } from "../data/profileData";
import { useStateContext } from "../contexts/ContextProvider";
import profilePic from "../data/profilePic.png";

const UserProfile = () => {
  const { currentColor } = useStateContext();

  return (
    <div className="nav-item absolute right-1 top-16 bg-white dark:bg-[#42464D] p-8 rounded-lg w-96">
      <div className="flex justify-between items-center">
        <p className="font-semibold text-lg dark:text-gray-200">User Profile</p>
        <Button
          icon={<MdOutlineCancel />}
          color="rgb(153, 171, 180)"
          bgHoverColor="light-gray"
          size="2xl"
          borderRadius="50%"
        />
      </div>
      <div className="flex gap-5 items-center mt-6 border-color border-b-1 pb-6">
        <img
          className="rounded-full h-24 w-24"
          src={profilePic}
          alt="user-profile"
        />
        <div>
          <p className="font-semibold text-xl dark:text-gray-200">
            {" "}
            SeungGi Lee{" "}
          </p>
          <p className="text-gray-500 text-sm dark:text-gray-400">
            {" "}
            Administrator{" "}
          </p>
          <p className="text-gray-500 text-sm font-semibold dark:text-gray-400">
            {" "}
            acvart123123@gmail.com{" "}
          </p>
        </div>
      </div>
      <div className="mt-5">
        <Button
          color="white"
          bgColor={currentColor}
          text="Logout"
          borderRadius="10px"
          width="full"
        />
      </div>
    </div>
  );
};

export default UserProfile;
