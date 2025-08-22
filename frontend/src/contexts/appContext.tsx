import React, { PropsWithChildren } from "react";

export interface NotificationDataType {
  notificationType: {
    icon: boolean;
    style: "none" | "info" | "success" | "warning" | "error";
  };
  message: string;
}

export type AppContextType = {
  showNotification: (notificationData: NotificationDataType) => void;
  closeNotification: () => void;
};

const defaultContextValue: AppContextType = {
  showNotification: () => {},
  closeNotification: () => {},
};

export const AppContext =
  React.createContext<AppContextType>(defaultContextValue);

interface AppContextProviderProps extends PropsWithChildren {
  showNotification: (notificationData: NotificationDataType) => void;
  closeNotification: () => void;
}

export const AppContextProvider: React.FC<AppContextProviderProps> = ({
  children,
  showNotification,
  closeNotification,
}: AppContextProviderProps) => {
  const value = React.useMemo(
    () => ({
      showNotification,
      closeNotification,
    }),
    [showNotification, closeNotification]
  );

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
