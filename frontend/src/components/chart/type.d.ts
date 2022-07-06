import { Trend, TrendData } from "../../models";
//type of chart parameeters


export type ChartParams = {
    mode:ChartMode,
    grid_lines: GridLines,
    //is_loading_data:boolean,
    is_loading_trends:boolean,
    refArea:{
       left:number,
       right:number 
    },
    cfgRange  : ChartRange,
    currRange : ChartRange,
    data : ITrendData[],
    lastUpdated : number,
   // series : ChartSerie[]
    trends :  ITrend[],
    brush:{startIndex:number, endIndex:number},
    force_refresh : boolean
   // size : ISize  // chart size
  }

  export type ITrendData = TrendData & {
    unixtime : number
  }

  export type ITrend  = Trend  & {
    selected:boolean;
    axislabel:string;
    trendname:string;
    disabled:boolean;
  }
 
 /// export interface ITrend extends Trend {
  //  selected:boolan;
// }

 export type ChartMode ={
     zoom: boolean,
     tooltip: boolean,
     live: {
         active:boolean,
         timer:NodeJS.Timer | undefined,
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
