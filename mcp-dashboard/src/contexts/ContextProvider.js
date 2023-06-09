import React, { createContext, useContext, useState } from "react";

const StateContext = createContext();

const initialState = {
  userProfile: false,
  notification: false,
};

export const ContextProvider = ({ children }) => {
  const [isClicked, setIsClicked] = useState(initialState);
  const [isAuthorized, setIsAuthorized] = useState(localStorage.getItem("accessToken"));
  const [stacks, setStacks] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [checkedInputs, setCheckedInputs] = useState([]);
  const [parameters, setParameters] = useState({});
  const [deployDetail, setDeployDetail] = useState([]);

  const mainColor = "#03C9D7";
  const disabledColor = "#E5E7Eb";
  const base_url = 'http://localhost:8000';
  const handleClick = (clicked) =>
    setIsClicked({ ...initialState, [clicked]: true });

  return (
    // eslint-disable-next-line react/jsx-no-constructed-context-values
    <StateContext.Provider
      value={{
        mainColor,
        disabledColor,
        handleClick,
        isClicked,
        initialState,
        setIsClicked,
        base_url,
        stacks,
        setStacks,
        isAuthorized,
        setIsAuthorized,
        isModalOpen,
        setIsModalOpen,
        checkedInputs,
        setCheckedInputs,
        parameters,
        setParameters,
        deployDetail,
        setDeployDetail,
      }}
    >
      {children}
    </StateContext.Provider>
  );
};

export const useStateContext = () => useContext(StateContext);
