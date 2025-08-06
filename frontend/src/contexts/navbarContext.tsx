import React, { PropsWithChildren } from "react";

export type NavbarContextType = {
  setTitle: (title: string) => void;
  useMockup: boolean;
};

const defaultContextValue: NavbarContextType = {
  setTitle: () => {},
  useMockup: false,
};

export const NavbarContext =
  React.createContext<NavbarContextType>(defaultContextValue);

interface NavbarContextProviderProps extends PropsWithChildren {
  setTitle: (title: string) => void;
  useMockup: boolean;
}

export const NavbarContextProvider: React.FC<NavbarContextProviderProps> = ({
  children,
  setTitle,
  useMockup,
}: NavbarContextProviderProps) => {
  const value = React.useMemo(
    () => ({
      setTitle,
      useMockup,
    }),
    [setTitle, useMockup]
  );

  return (
    <NavbarContext.Provider value={value}>{children}</NavbarContext.Provider>
  );
};
