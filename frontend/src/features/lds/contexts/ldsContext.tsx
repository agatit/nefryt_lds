import React, { PropsWithChildren } from "react";
import {
  Trend,
  TrendApi,
  TrendDefBase,
  TrendGroup,
  TrendGroupApi,
  Unit,
  UnitApi,
} from "../../../services/api";

export type LDSContextType = {
  trendDefs: TrendDefBase[];
  trendApi: TrendApi;
  trends: Trend[];
  setTrends: (value: Trend[]) => void;
  trendGroupApi: TrendGroupApi;
  trendGroups: TrendGroup[];
  setTrendGroups: (value: TrendGroup[]) => void;
  unitApi: UnitApi;
  units: Unit[];
  setUnits: (value: Unit[]) => void;
};

export const LDSContext = React.createContext<LDSContextType | null>(null);

interface LDSContextProviderProps extends PropsWithChildren {
  trendDefs: TrendDefBase[];
  trendApi: TrendApi;
  trends: Trend[];
  setTrends: (value: Trend[]) => void;
  trendGroupApi: TrendGroupApi;
  trendGroups: TrendGroup[];
  setTrendGroups: (value: TrendGroup[]) => void;
  unitApi: UnitApi;
  units: Unit[];
  setUnits: (value: Unit[]) => void;
}

export const LDSContextProvider: React.FC<LDSContextProviderProps> = ({
  children,
  trendDefs,
  trendApi,
  trends,
  setTrends,
  trendGroupApi,
  trendGroups,
  setTrendGroups,
  unitApi,
  units,
  setUnits,
}: LDSContextProviderProps) => {
  const value = React.useMemo(
    () => ({
      trendDefs,
      trendApi,
      trends,
      setTrends,
      trendGroupApi,
      trendGroups,
      setTrendGroups,
      unitApi,
      units,
      setUnits,
    }),
    [trendDefs, trendApi, trends, trendGroupApi, trendGroups, unitApi, units]
  );

  return <LDSContext.Provider value={value}>{children}</LDSContext.Provider>;
};
