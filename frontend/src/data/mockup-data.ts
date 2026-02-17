import {
  AxisType,
  TreeViewDataItem,
} from "../features/lds/features/trends/components/utils";
import {
  Template,
  Trend,
  TrendDef,
  TrendGroup,
  TrendParamDef,
  Unit,
  Event,
  Link,
  EventDef,
  Node,
  Pipeline,
  PipelineParam,
  Method,
  MethodDef,
  MethodParam,
  MethodParamDef,
} from "../services/api";

// export type MockupTrendType = {
//   ID: number;
//   TrendGroupID: number;
//   Color: string;
//   TrendDefID: string;
//   Name: string;
//   Unit: string;
// };

export const mockupTrendDefs: TrendDef[] = [
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
    UnitID: "C_s",
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
    UnitID: "C_s",
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

export const mockupTrendParamDefs: TrendParamDef[] = [
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

export const mockupEvents: Event[] = [
  {
    ID: 1,
    EventDefID: "TEST",
    MethodID: 1,
    BeginDate: new Date("2026-02-04T08:00:00Z").toISOString(),
    AckDate: new Date("2026-02-04T08:05:00Z").toISOString(),
    EndDate: new Date("2026-02-04T08:10:00Z").toISOString(),
    Details: "Pipeline pressure exceeded threshold",
    Position: 1,
    Verbosity: "INFO",
    Caption: "Pressure warning",
    Silent: false,
  },
  {
    ID: 2,
    EventDefID: "ALARM",
    MethodID: 2,
    BeginDate: new Date("2026-02-04T09:15:00Z").toISOString(),
    AckDate: null,
    EndDate: null,
    Details: "Leak detected near valve A3",
    Position: 3,
    Verbosity: "ERROR",
    Caption: "Leak detected",
    Silent: false,
  },
  {
    ID: 3,
    EventDefID: "SYSTEM",
    MethodID: 3,
    BeginDate: new Date("2026-02-04T10:30:00Z").toISOString(),
    AckDate: new Date("2026-02-04T10:32:00Z").toISOString(),
    EndDate: null,
    Details: "System entered maintenance mode",
    Position: 0,
    Verbosity: "INFO",
    Caption: "Maintenance mode",
    Silent: true,
  },
  {
    ID: 4,
    EventDefID: "WARNING",
    MethodID: 4,
    BeginDate: new Date("2026-02-04T11:45:00Z").toISOString(),
    AckDate: null,
    EndDate: null,
    Details: "Temperature approaching critical level",
    Position: 2,
    Verbosity: "WARN",
    Caption: "High temperature",
    Silent: false,
  },
];

export const mockupLinks: Link[] = [
  {
    ID: 1,
    BeginNodeID: 10,
    EndNodeID: 20,
    Length: "125.5",
  },
  {
    ID: 2,
    BeginNodeID: 20,
    EndNodeID: 30,
    Length: "98.3",
  },
  {
    ID: 3,
    BeginNodeID: 30,
    EndNodeID: 40,
    Length: "210.0",
  },
];

export const mockupEventDefs: EventDef[] = [
  {
    ID: "ANOMALY",
    Caption: "Detekcja anomalii",
    Enabled: true,
    Verbosity: "WARNING",
    Silent: false,
    Visible: true,
  },
  {
    ID: "LEAK",
    Caption: "Detekcja wycieku",
    Enabled: true,
    Verbosity: "ALARM",
    Silent: false,
    Visible: true,
  },
  {
    ID: "NO_DATA",
    Caption: "Brak danych do detekcji",
    Enabled: true,
    Verbosity: "WARNING",
    Silent: false,
    Visible: true,
  },
  {
    ID: "START",
    Caption: "Uruchomienie detekcji",
    Enabled: true,
    Verbosity: "INFO",
    Silent: false,
    Visible: false,
  },
  {
    ID: "STOP",
    Caption: "Zatrzymanie detekcji",
    Enabled: true,
    Verbosity: "INFO",
    Silent: false,
    Visible: false,
  },
];

export const mockupNodes: Node[] = [
  {
    Type: "PRESS",
    Name: "PT-01",
    EditorParams: null,
    TrendID: null,
    ID: 1,
  },
  {
    Type: "PRESS",
    Name: "PT-02",
    EditorParams: null,
    TrendID: null,
    ID: 2,
  },
  {
    Type: "PRESS",
    Name: "PT-03",
    EditorParams: null,
    TrendID: null,
    ID: 3,
  },
  {
    Type: "PRESS",
    Name: "PT-04",
    EditorParams: null,
    TrendID: null,
    ID: 4,
  },
];

export const mockupPipelines: Pipeline[] = [
  {
    ID: 1,
    Name: "Zygmuntow_1",
  },
];

export const mockupPipelineParams: PipelineParam[] = [
  {
    PipelineParamDefID: "ACTIVE_METHODS",
    Value: "20,1001",
    PipelineID: 1,
    DataType: "LIST",
    Name: "Metody generujące zdarzenia",
  },
  {
    PipelineParamDefID: "BEGIN_POS",
    Value: "3.31",
    PipelineID: 1,
    DataType: "INT",
    Name: "Pozycja poczatkowa [m]",
  },
  {
    PipelineParamDefID: "FIRST_NODE_ID",
    Value: "4",
    PipelineID: 1,
    DataType: "INT",
    Name: "First node ID",
  },
  {
    PipelineParamDefID: "LENGTH_RESOLUTION",
    Value: "10",
    PipelineID: 1,
    DataType: "INT",
    Name: "Rozdzielczość w pozycji [m]",
  },
  {
    PipelineParamDefID: "TIME_RESOLUTION",
    Value: "1000",
    PipelineID: 1,
    DataType: "INT",
    Name: "Rozdzielczość w czasie [ms]",
  },
];

export const mockupMethods: Method[] = [
  {
    PipelineID: 1,
    Name: "Fali",
    ID: 20,
    MethodDefID: "WAVE",
  },
  {
    PipelineID: 1,
    Name: "Test TOF",
    ID: 1001,
    MethodDefID: "TOF",
  },
];

export const mockupMethodDefs: MethodDef[] = [
  {
    Name: "Matoda bilansu",
    ID: "BALANCE",
  },
  {
    Name: "Wynik łączny",
    ID: "COMBINE",
  },
  {
    Name: "Zaślepka",
    ID: "DUMMY",
  },
  {
    Name: "Maskowanie zdarzeń tech.",
    ID: "MASK",
  },
  {
    Name: "Metoda czasu przypływu",
    ID: "TOF",
  },
  {
    Name: "Metoda fali",
    ID: "WAVE",
  },
];

export const mockupMethodParamDef: MethodParamDef[] = [
  {
    DataType: "REAL",
    ID: "ALARM_LEVEL",
    MethodDefID: "BALANCE",
    Name: "AlarmLevel",
  },
  {
    DataType: "REAL",
    ID: "ALARM_LEVEL",
    MethodDefID: "WAVE",
    Name: "AlarmLevel",
  },
  {
    DataType: "REAL",
    ID: "BASE_WAVE_SPEED",
    MethodDefID: "TOF",
    Name: "BaseWaveSpeed",
  },
  {
    DataType: "REAL",
    ID: "BASE_WAVE_SPEED",
    MethodDefID: "WAVE",
    Name: "BaseWaveSpeed",
  },
  {
    DataType: "REAL",
    ID: "CONSTANT_CORRECTION",
    MethodDefID: "BALANCE",
    Name: "ConstantCorrection",
  },
  {
    DataType: "TREND",
    ID: "DENSITY_TREND_1",
    MethodDefID: "BALANCE",
    Name: "DensityTrend1",
  },
];

export const mockupMethodParams: MethodParam[] = [
  {
    MethodParamDefID: "ALARM_LEVEL",
    Value: "0.06",
    MethodID: 20,
    DataType: "REAL",
    Name: "AlarmLevel",
  },
  {
    MethodParamDefID: "BASE_WAVE_SPEED",
    Value: "425",
    MethodID: 20,
    DataType: "REAL",
    Name: "BaseWaveSpeed",
  },
  {
    MethodParamDefID: "LEAKAGE_LEVEL",
    Value: "0.02",
    MethodID: 20,
    DataType: "REAL",
    Name: "LeakageLevel",
  },
  {
    MethodParamDefID: "LEAKAGE_WINDOW",
    Value: "2000",
    MethodID: 20,
    DataType: "REAL",
    Name: "LeakageWindow",
  },
  {
    MethodParamDefID: "MIN_WAVE_VALUE",
    Value: "10",
    MethodID: 20,
    DataType: "REAL",
    Name: "MinWaveValue",
  },
  {
    MethodParamDefID: "NO_DETECTION_WINDOW",
    Value: "10",
    MethodID: 20,
    DataType: "REAL",
    Name: "NoDetectionWindow",
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
