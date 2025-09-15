import React, { PropsWithChildren } from "react";
import {
  Trend,
  TrendApi,
  TrendDef,
  TrendGroup,
  TrendGroupApi,
  TrendParamApi,
  TrendParamDef,
  Unit,
  UnitApi,
} from "../../../services/api";

export type LDSContextType = {
  trendDefs: TrendDef[];
  trendApi: TrendApi;
  trends: Trend[];
  setTrends: (value: Trend[]) => void;
  addTrend: (value: Trend) => Promise<Trend>;
  updateTrend: (value: Trend) => Promise<void>;
  deleteTrend: (value: Trend) => Promise<void>;
  trendParamApi: TrendParamApi;
  trendParamDefs: TrendParamDef[];
  trendGroupApi: TrendGroupApi;
  trendGroups: TrendGroup[];
  setTrendGroups: (value: TrendGroup[]) => void;
  addTrendGroup: (value: TrendGroup) => Promise<void>;
  updateTrendGroup: (value: TrendGroup) => Promise<void>;
  deleteTrendGroup: (value: TrendGroup) => Promise<void>;
  unitApi: UnitApi;
  units: Unit[];
  setUnits: (value: Unit[]) => void;
  addUnit: (value: Unit) => Promise<void>;
  updateUnit: (value: Unit) => Promise<void>;
  deleteUnit: (value: Unit) => Promise<void>;
};

export const LDSContext = React.createContext<LDSContextType | null>(null);

interface LDSContextProviderProps extends PropsWithChildren {
  trendDefs: TrendDef[];
  trendApi: TrendApi;
  trends: Trend[];
  setTrends: (value: Trend[]) => void;
  addTrend: (value: Trend) => Promise<Trend>;
  updateTrend: (value: Trend) => Promise<void>;
  deleteTrend: (value: Trend) => Promise<void>;
  trendParamApi: TrendParamApi;
  trendParamDefs: TrendParamDef[];
  trendGroupApi: TrendGroupApi;
  trendGroups: TrendGroup[];
  setTrendGroups: (value: TrendGroup[]) => void;
  addTrendGroup: (value: TrendGroup) => Promise<void>;
  updateTrendGroup: (value: TrendGroup) => Promise<void>;
  deleteTrendGroup: (value: TrendGroup) => Promise<void>;
  unitApi: UnitApi;
  units: Unit[];
  setUnits: (value: Unit[]) => void;
  addUnit: (value: Unit) => Promise<void>;
  updateUnit: (value: Unit) => Promise<void>;
  deleteUnit: (value: Unit) => Promise<void>;
}

export const LDSContextProvider: React.FC<LDSContextProviderProps> = ({
  children,
  trendDefs,
  trendApi,
  trends,
  setTrends,
  addTrend,
  updateTrend,
  deleteTrend,
  trendParamApi,
  trendParamDefs,
  trendGroupApi,
  trendGroups,
  setTrendGroups,
  addTrendGroup,
  updateTrendGroup,
  deleteTrendGroup,
  unitApi,
  units,
  setUnits,
  addUnit,
  updateUnit,
  deleteUnit,
}: LDSContextProviderProps) => {
  const value = React.useMemo(
    () => ({
      trendDefs,
      trendApi,
      trends,
      setTrends,
      addTrend,
      updateTrend,
      deleteTrend,
      trendParamApi,
      trendParamDefs,
      trendGroupApi,
      trendGroups,
      setTrendGroups,
      addTrendGroup,
      updateTrendGroup,
      deleteTrendGroup,
      unitApi,
      units,
      setUnits,
      addUnit,
      updateUnit,
      deleteUnit,
    }),
    [
      trendDefs,
      trendApi,
      trends,
      addTrend,
      updateTrend,
      deleteTrend,
      trendParamApi,
      trendParamDefs,
      trendGroupApi,
      trendGroups,
      addTrendGroup,
      updateTrendGroup,
      deleteTrendGroup,
      unitApi,
      units,
      addUnit,
      updateUnit,
      deleteUnit,
    ]
  );

  return <LDSContext.Provider value={value}>{children}</LDSContext.Provider>;
};
