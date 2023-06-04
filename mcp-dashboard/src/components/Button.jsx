import React from "react";
import { useNavigate } from "react-router-dom";
import { useStateContext } from "../contexts/ContextProvider";

const Button = ({
  icon,
  bgColor,
  color,
  bgHoverColor,
  size,
  text,
  borderRadius,
  width,
  onClickFunc,
  type,
  disabled
}) => {
  const { setIsClicked, initialState } = useStateContext();
  const navigate = useNavigate();
  return (
    <button
      type={type}
      onClick={onClickFunc}
      style={{ backgroundColor: bgColor, color, borderRadius }}
      className={disabled ? `text-${size} p-3 w-${width}` : `text-${size} p-3 w-${width} hover:drop-shadow-xl hover:bg-${bgHoverColor}`}
      disabled={disabled}
    >
      {icon} {text}
    </button>
  );
};

export default Button;
