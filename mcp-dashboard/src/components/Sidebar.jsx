import React from "react";
import { Link, NavLink } from "react-router-dom";
import { AiTwotoneCloud } from "react-icons/ai";
import { links } from "../data/links";
import { useStateContext } from "../contexts/ContextProvider";

const Sidebar = () => {
  const { mainColor, activeMenu, setActiveMenu } =
    useStateContext();

  const activeLink =
    "flex items-center gap-5 pl-4 pt-3 pb-2.5 rounded-lg  text-white  text-md m-2";
  const normalLink =
    "flex items-center gap-5 pl-4 pt-3 pb-2.5 rounded-lg text-md text-gray-700 dark:text-gray-200 dark:hover:text-black hover:bg-light-gray m-2";

  return (
    <div className="ml-3 h-screen md:overflow-hidden overflow-auto md:hover:overflow-auto pb-10">
      <>
        <div className="flex justify-between items-center">
          <Link
            to="/dashboard"
            className="items-center gap-3 ml-3 mt-4 flex text-xl font-extrabold tracking-tight dark:text-white text-slate-900"
          >
            <AiTwotoneCloud /> <span>Multi Cloud Platform</span>
          </Link>

        </div>
        <div className="mt-10">
          {links.map((item) => (
            <div key={item.title}>
              <p className="text-gray-400 dark:text-gray-400 m-3 mt-4 uppercase">
                {item.title}
              </p>
              {item.links.map((link) => (
                <NavLink
                  to={`/${link.value}`}
                  key={link.name}
                  style={({ isActive }) => ({
                    backgroundColor: isActive ? mainColor : "",
                  })}
                  className={({ isActive }) =>
                    isActive ? activeLink : normalLink
                  }
                >
                  {link.icon}
                  <span className="capitalize ">{link.name}</span>
                </NavLink>
              ))}
            </div>
          ))}
        </div>
      </>
    </div>
  );
};

export default Sidebar;
