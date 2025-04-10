import React, { PropsWithChildren } from "react";

export type NavbarContextType = {
  setTitle: (title: string) => void;
};

export const NavbarContext = React.createContext<NavbarContextType | null>(
  null
);

interface NavbarContextProviderProps extends PropsWithChildren {
  setTitle: (title: string) => void;
}

export const NavbarContextProvider = (props: NavbarContextProviderProps) => {
  function setTitle(title: string) {
    props.setTitle(title);
  }

  return (
    <NavbarContext.Provider value={{ setTitle }}>
      {props.children}
    </NavbarContext.Provider>
  );
};
