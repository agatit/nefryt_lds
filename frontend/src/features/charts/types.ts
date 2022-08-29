import { Trend, TrendData } from "../../store/trendApi";

export const PERIOD_EXTENSION = 2;


export type ChartsState = {
    chart : ChartParams
    rpanel_open : boolean,
}

export type ChartParams = {
    mode:ChartMode,
    grid_lines: GridLines,
    is_loading_trends:boolean,
    refArea:{
       left:number,
       right:number 
    },
    cfgRange  : ChartRange,
    currRange : ChartRange,
    data : ITrendData[],
    lastUpdated : number,
    onlySelected : boolean,
    trends :  ITrend[],
    brush:{startIndex:number, endIndex:number},
    force_refresh : boolean
  }

  export type ITrendData = TrendData & {
    unixtime : number
  }

  export type ITrend  = Trend  & {
    selected:boolean;
    axislabel:string;
    trendname:string;
    disabled:boolean;
    autoscale:boolean;
    scale:{min:number, max:number};
    marks:{value:number, label:string}[];
    step:number;
  }
 

 export type ChartMode ={
     zoom: boolean,
     tooltip: boolean,
     live: {
         active:boolean,
         timer:NodeJS.Timer | undefined,
         period : number
        }
 } 

 export type GridLines={
    h:boolean
    v:boolean
}

export type ChartRange = {
    from : number,
    to : number 
}
  

export type IChartAction ={
    type: string
    data :  any
}
