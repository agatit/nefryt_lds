import {
  AxisType,
  TreeViewDataItem,
} from "../features/lds/features/trends_page/TrendsPage";
import {
  Template,
  Trend,
  TrendDefBase,
  TrendGroup,
  Unit,
} from "../services/api";

// export type MockupTrendType = {
//   ID: number;
//   TrendGroupID: number;
//   Color: string;
//   TrendDefID: string;
//   Name: string;
//   Unit: string;
// };

export const mockupTrendDefs: TrendDefBase[] = [
  {
    ID: "QUICK",
    Name: "Point series trend",
  },
  {
    ID: "DERIV",
    Name: "Derivative",
  },
  {
    ID: "DIFF",
    Name: "Difference",
  },
  {
    ID: "MEAN",
    Name: "Mean filter",
  },
];

export const mockupTrendGroups: TrendGroup[] = [
  {
    ID: 1,
    Name: "Ciśnienie",
  },
  {
    ID: 2,
    Name: "Temperatura",
  },
];

export const mockupTrends: Trend[] = [
  {
    ID: 0,
    TrendGroupID: 1,
    Color: "#ff6358",
    TrendDefID: "QUICK",
    Name: "Ciśnienie 1",
    UnitID: "MPa",
    RawMin: 0,
    RawMax: 10,
    ScaledMin: 0,
    ScaledMax: 10,
  },
  {
    ID: 1,
    TrendGroupID: 1,
    Color: "#ffe162",
    TrendDefID: "QUICK",
    Name: "Ciśnienie 2",
    UnitID: "MPa",
    RawMin: 0,
    RawMax: 10,
    ScaledMin: 0,
    ScaledMax: 10,
  },
  {
    ID: 2,
    TrendGroupID: 1,
    Color: "#4cd180",
    TrendDefID: "QUICK",
    Name: "Ciśnienie 3",
    UnitID: "MPa",
    RawMin: 0,
    RawMax: 10,
    ScaledMin: 0,
    ScaledMax: 10,
  },
  {
    ID: 3,
    TrendGroupID: 1,
    Color: "#4b5ffa",
    TrendDefID: "DERIV",
    Name: "Pochodna Ciśnienia 1",
    UnitID: "MPa_s",
    RawMin: 0,
    RawMax: 10,
    ScaledMin: 0,
    ScaledMax: 10,
  },
  {
    ID: 4,
    TrendGroupID: 1,
    Color: "#ac58ff",
    TrendDefID: "DERIV",
    Name: "Pochodna Ciśnienia 2",
    UnitID: "MPa_s",
    RawMin: 0,
    RawMax: 10,
    ScaledMin: 0,
    ScaledMax: 10,
  },
  {
    ID: 5,
    TrendGroupID: 2,
    Color: "#ff5892",
    TrendDefID: "QUICK",
    Name: "Temperatura 1",
    UnitID: "C",
    RawMin: 0,
    RawMax: 10,
    ScaledMin: 0,
    ScaledMax: 10,
  },
  {
    ID: 6,
    TrendGroupID: 2,
    Color: "#59ffc4",
    TrendDefID: "QUICK",
    Name: "Temperatura 2",
    UnitID: "C",
    RawMin: 0,
    RawMax: 10,
    ScaledMin: 0,
    ScaledMax: 10,
  },
  {
    ID: 7,
    TrendGroupID: 2,
    Color: "#ffc459",
    TrendDefID: "DERIV",
    Name: "Pochodna Temperatury 1",
    UnitID: "°C_s",
    RawMin: 0,
    RawMax: 10,
    ScaledMin: 0,
    ScaledMax: 10,
  },
  {
    ID: 8,
    TrendGroupID: 2,
    Color: "#4b9dd1",
    TrendDefID: "DERIV",
    Name: "Pochodna Temperatury 2",
    UnitID: "°C_s",
    RawMin: 0,
    RawMax: 10,
    ScaledMin: 0,
    ScaledMax: 10,
  },
];

export const mockupTrendTreeData: TreeViewDataItem[] = [
  {
    id: 1,
    text: "Ciśnienie",
    items: [
      {
        id: 2,
        text: "Pomiary",
        items: [
          { text: mockupTrends[0].Name!, id: mockupTrends[0].ID },
          { text: mockupTrends[1].Name!, id: mockupTrends[1].ID },
          { text: mockupTrends[2].Name!, id: mockupTrends[2].ID },
        ],
      },
      {
        id: 3,
        text: "Pochodne",
        items: [
          { text: mockupTrends[3].Name!, id: mockupTrends[3].ID },
          { text: mockupTrends[4].Name!, id: mockupTrends[4].ID },
        ],
      },
    ],
  },
  {
    id: 4,
    text: "Temperatura",
    items: [
      {
        id: 5,
        text: "Pomiary",
        items: [
          { text: mockupTrends[5].Name!, id: mockupTrends[5].ID },
          { text: mockupTrends[6].Name!, id: mockupTrends[6].ID },
        ],
      },
      {
        id: 6,
        text: "Pochodne",
        items: [
          { text: mockupTrends[7].Name!, id: mockupTrends[7].ID },
          { text: mockupTrends[8].Name!, id: mockupTrends[8].ID },
        ],
      },
    ],
  },
];

export const mockupAxes: AxisType[] = [
  {
    Name: "Ciśnienie pomiary MPa",
    Unit: "MPa",
    TrendIDs: [0, 1, 2],
    ScaleMax: 9,
    ScaleMin: -1,
  },
];

export const mockupUnits: Unit[] = [
  {
    ID: "C",
    Name: "Temperatura",
    Symbol: "°C",
    BaseID: "C",
    Multiplier: "1.0",
  },
  {
    ID: "MPa",
    Name: "Ciśnienie",
    Symbol: "MPa",
    BaseID: "MPa",
    Multiplier: "1.0",
  },
  {
    ID: "C_s",
    Name: "Pochodna temperatury",
    Symbol: "°C/s",
    BaseID: "C_s",
    Multiplier: "1.0",
  },
  {
    ID: "MPa_s",
    Name: "Pochodna ciśnienia",
    Symbol: "MPa/s",
    BaseID: "MPa_s",
    Multiplier: "1.0",
  },
];

export const mockupTemplates: Template[] = [
  {
    Name: "Pomiary ciśnień",
    Axes: [
      {
        TrendsID: [0, 1, 2],
        Title: "Ciśnienie",
        UnitID: "MPa",
        ScaledMin: -4,
        ScaledMax: 12,
      },
    ],
    ID: 0,
  },
  {
    Name: "Ciśnienia wszystko",
    Axes: [
      {
        TrendsID: [0, 1, 2],
        Title: "Ciśnienie",
        UnitID: "MPa",
        ScaledMin: -4,
        ScaledMax: 12,
      },
      {
        TrendsID: [3, 4],
        Title: "Pochodna",
        UnitID: "MPa_s",
        ScaledMin: -4,
        ScaledMax: 12,
      },
    ],
    ID: 1,
  },
];

export interface MockupTrendGroupType {
  ID: number;
  Name: string;
  AnalisisOnly?: boolean;
}

export const mockupTrendGroupFromDB: MockupTrendGroupType[] = [
  {
    ID: 1,
    Name: "Przepływ",
  },
  {
    ID: 2,
    Name: "Temperatura",
  },
  {
    ID: 3,
    Name: "Gęstość",
  },
  {
    ID: 4,
    Name: "Ciśnienie",
  },
  {
    ID: 6,
    Name: "Przepływ",
  },
  {
    ID: 7,
    Name: "Temperatura",
  },
  {
    ID: 8,
    Name: "Gęstość",
  },
  {
    ID: 9,
    Name: "Ciśnienie",
  },
  {
    ID: 10,
    Name: "Automatyka",
  },
  {
    ID: 11,
    Name: "Automatyka",
  },
];

export interface MockupTrendParamDefType {
  ID: string;
  TrendDefID: string;
  Name: string;
  DataType: string;
}

export const mockupTrendParamDefs: MockupTrendParamDefType[] = [
  {
    ID: "FILTER_WINDOW",
    TrendDefID: "DERIV",
    Name: "Okno filtrowania",
    DataType: "INT",
  },
  {
    ID: "FILTER_WINDOW",
    TrendDefID: "MEAN",
    Name: "Okno filtrowania",
    DataType: "INT",
  },
  {
    ID: "MODBUS_REGISTER",
    TrendDefID: "QUICK",
    Name: "Rejestr modbus",
    DataType: "INT",
  },
  {
    ID: "TREND_A",
    TrendDefID: "DIFF",
    Name: "TrendID A",
    DataType: "TREND",
  },
  {
    ID: "TREND_B",
    TrendDefID: "DIFF",
    Name: "TrendID B",
    DataType: "TREND",
  },
];
