import React, { useEffect } from "react";
import { RiNotification3Line } from "react-icons/ri";
import { MdKeyboardArrowDown } from "react-icons/md";

import profilePic from "../data/profilePic.png";
import { UserProfile, Notification } from ".";
import { useStateContext } from "../contexts/ContextProvider";

const NavButton = ({ onClickFunc, icon, color, dotColor }) => (
  <button
    type="button"
    onClick={() => onClickFunc()}
    style={{ color }}
    className="relative text-xl rounded-full p-3 hover:bg-light-gray"
  >
    <span
      style={{ background: dotColor }}
      className="absolute inline-flex rounded-full h-2 w-2 right-2 top-2"
    />
    {icon}
  </button>
);

const Navbar = () => {
  const {
    mainColor,
    handleClick,
    isClicked,
    isAuthorized,
    setIsAuthorized
  } = useStateContext();

  return (
    <div className="flex justify-end p-2 md:ml-6 md:mr-6 relative">
      <div className="flex">

        <NavButton
          dotColor="#EA4336"
          onClickFunc={() => handleClick("notification")}
          color={mainColor}
          icon={<RiNotification3Line />}
        />
        <div
          className="flex items-center gap-2 cursor-pointer p-1 hover:bg-light-gray rounded-lg ml-4"
          onClick={() => handleClick("userProfile")}
        >
          <img
            className="rounded-full w-8 h-8"
            src={profilePic}
            alt="user-profile"
          />
          <p>
            <span className="text-gray-400 text-14 font-bold">
              {localStorage.getItem("username")}
            </span>
            <span className="text-gray-400 font-bold ml-1 text-15">
            </span>
          </p>
          <MdKeyboardArrowDown className="text-gray-400 text-14" />
        </div>

        {isClicked.notification && <Notification />}
        {isClicked.userProfile && <UserProfile />}
      </div>
    </div>
  );
};

export default Navbar;
