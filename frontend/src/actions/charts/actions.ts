
import { TwoMpTwoTone } from "@mui/icons-material";
import { ChartRange, IChartAction, ITrend } from "../../components/chart/type";
import { ADD_SERIE, APPEND_DATA, AREA_REF,  H_GRID_LINE,   REMOVE_SERIE,  SET_DATA,  SET_FROM_DATE,  SET_TIMER, SET_TO_DATE,  LOAD_TREND_LIST,  TOGGLE_LIVE_MODE, TOGGLE_RPANEL, TOGGLE_TOOLTIP, TOGGLE_ZOOM_MODE, V_GRID_LINE, SET_DATE_RANGE, SET_TIMESTAMP_RANGE, ENABLE_TREND, DISABLE_TREND, SET_BRUSH_RANGE} from "./actionType";




function getData(beginDate : number, endDate:number, DATA_SIZE : number, trends : ITrend[]): any {

  setTimeout(
    function() {

 
    let data = [];

    const data3 = [
      {
        name: 'Page A',
        uv: 4000,
        pv: 2400,
        amt: 2400,
      },
      {
        name: 'Page B',
        uv: 3000,
        pv: 1398,
        amt: 2210,
      },
      {
        name: 'Page C',
        uv: 2000,
        
        amt: 2290,
      },
      {
        name: 'Page D',
        uv: 2780,
        
        amt: 2000,
      },
      {
        name: 'Page E',
        uv: 1890,
        pv: 4800,
        amt: 2181,
      },
      {
        name: 'Page F',
        uv: 2390,
        pv: 3800,
        amt: 2500,
      },
      {
        name: 'Page G',
        uv: 3490,
        pv: 4300,
        amt: 2100,
      },
    ];

    var range = Math.round((endDate - beginDate)/DATA_SIZE);
    
    if (range==0){
      range++;
    }

    for (let i = beginDate; i < beginDate+(DATA_SIZE*range); i=i+range) {
      var dat : any = {name:i};
       trends.map(trend => {
           dat[trend.iD] = Math.random() * 1000;
       });
       data.push(dat);
    }

  }, 5000);

    
}

export function setHorizontalLine(visible:boolean) {
  const action: IChartAction = {
    type: H_GRID_LINE,
    data : visible
  }
  return action;
}

export function setVerticalLine(visible:boolean) {
  const action: IChartAction = {
    type: V_GRID_LINE,
    data : visible
  }
  return action;
}

export function toggleLiveMode() {
  const action: IChartAction = {
    type: TOGGLE_LIVE_MODE,
    data : null
  }
  return action;
}

export function toggleTooltip() {
  const action: IChartAction = {
    type: TOGGLE_TOOLTIP,
    data : null
  }
  return action;
}

export function toggleZoomMode() {
  const action: IChartAction = {
    type: TOGGLE_ZOOM_MODE,
    data : null
  }
  return action;
}



export function toggleRightPanel() {
  const action: IChartAction = {
    type: TOGGLE_RPANEL,
    data : null
  }
  return action;
}
/*
export function setGridMode(zoomable:boolean) {
  const action: IChartAction = {
    type: GRID_MODE,
    data : zoomable
  }
  return action;
}
*/
/*
export function setTimeRange(range:ChartRange) {
  const action: IChartAction = {
    type: TIME_RANGE,
    data : range
  }
  return action;
}
*/

export function appendData(data:any) {
 
  const action: IChartAction = {
    type: APPEND_DATA,
    data : data
  }
  return action;
}

export function setTimer(data:NodeJS.Timer | undefined) {
 
  const action: IChartAction = {
    type: SET_TIMER,
    data : data
  }
  return action;
}

export function areaRef(data:any) {
 
  const action: IChartAction = {
    type: AREA_REF,
    data : data
  }
  return action;
}
  

/*
export function setSeries(series:ChartSerie[]) {
  const action: IChartAction = {
    type: SET_SERIES,
    data : series
  }
  return action;
}


export function addSerie(name:string) {
  const action: IChartAction = {
    type: ADD_SERIE,
    data : name
  }
  return action;
}

export function removeSerie(name:string) {
  const action: IChartAction = {
    type: REMOVE_SERIE,
    data : name
  }
  return action;
}

export function setChartSize(size:ISize) {
  const action: IChartAction = {
    type: CHART_SIZE,
    data : size
  }
  return action;
}
*/

/*
export const defaultArea:IDrawerArea = {bottom:0,left:0, right:0,top:0, innerWidth:0, innerHeight:0}
  
export const defaultZoom:IZoomData ={
  drawing:false,
  x_start:0,
  x_mode:false,
  y_mode:false,
  xy_mode:false,
  y_start:0
}

export function setSize(size:ChartSize) {
  const action: IChartAction = {
    type: SET_CHART_SIZE,
    data : size
  }
  return action;
}

export function changeTrendSeries(TrendName:string, selected : boolean) {
  const action: IChartAction = {
    type: selected ? ADD_SERIE : REMOVE_SERIE,
    data : TrendName
  }
  return action;
}




export function setDrawerArea(area:IDrawerArea) { 
  const action: IChartAction = {
    type: SET_DRAWER_AREA,
    data:area,
  }
  return action;
}


export function setDrawerZoom(zoom:IZoomData) {
 
  const action: IChartAction = {
    type: SET_DRAWER_AREA,
    data:zoom,
  }
  return action;
}


*/

export function enableTrend(trendiD:number) {
  const action: IChartAction = {
    type: ENABLE_TREND,
    data : trendiD
  }
  return action;
}

export function disableTrend(trendiD:number) {
  const action: IChartAction = {
    type: DISABLE_TREND,
    data : trendiD
  }
  return action;
}
export function setTrendList(data:any) {
 
  const action: IChartAction = {
    type: LOAD_TREND_LIST,
    data : data
  }
  return action;
}

export function setData(data:any, lastUpdated:number) {
 
  const action: IChartAction = {
    type: SET_DATA,
    data : {data: data, lastUpdated: lastUpdated}
  }
  return action;
}
 /*
export function loadData(is_load:boolean) {
  const action: IChartAction = {
    type: LOAD_DATA_STATE,
    data : is_load
  }
  return action;
}
*/
export function changeTrend(trendName:string, selected : boolean) {
  const action: IChartAction = {
    type: selected ? ADD_SERIE : REMOVE_SERIE,
    data : trendName
  }
  return action;
}



export function setTimestampRange(from:number, to:number) {
  const action: IChartAction = {
    type: SET_TIMESTAMP_RANGE,
    data : {from:from, to:to}
  }
  return action;
}

export function setBrushRange(from:number, to:number, startIndex:number, endIndex:number) {
  const action: IChartAction = {
    type: SET_BRUSH_RANGE,
    data : {from:from, to:to, startIndex:startIndex, endIndex:endIndex}
  }
  return action;
}

export function setDateRange() {
  const action: IChartAction = {
    type: SET_DATE_RANGE,
    data : null
  }
  return action;
}
  
export function setFromDate(date:any) {
  var tmp = Date.parse(date);
  const action: IChartAction = {
    type: SET_FROM_DATE,
    data : tmp
  }
  return action;
}

export function setToDate(date:any) {
  var tmp = Date.parse(date);
  const action: IChartAction = {
    type: SET_TO_DATE,
    data : tmp
  }
  return action;
}





