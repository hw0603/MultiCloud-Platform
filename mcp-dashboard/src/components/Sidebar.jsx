import React from "react";
import { Link, NavLink } from "react-router-dom";
import { links } from "../data/links.js";

const Sidebar = () => {
  return (
    <div>
    {links.map((item) => (
      <div key={item.title}>
        <p>{item.title}</p>
        {item.links.map((link) => (
          <NavLink
          to={`/${link.name}`}
          key={link.name}
          >
            {link.icon}
            <span>{link.name}</span>
          </NavLink>
        ))}
      </div>
    ))}
    </div>
  );
};

export default Sidebar;
