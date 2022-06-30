import { getDate } from "date-fns";
import { stat } from "fs";
import { ChartsState } from "../pages/Charts/type";
import { GridLines, IChartAction, ITrend, ITrendData } from "../components/chart/type";
import { ADD_SERIE, APPEND_DATA, AREA_REF,  DEFAULT_STATE,  DISABLE_TREND,  ENABLE_TREND,  H_GRID_LINE,  LOAD_DATA_STATE,  LOAD_TREND_LIST,  REMOVE_SERIE,  SET_DATA,  SET_DATE_RANGE,  SET_FROM_DATE,  SET_TIMER,  SET_TIMESTAMP_RANGE,  SET_TO_DATE,  TOGGLE_LIVE_MODE, TOGGLE_RPANEL, TOGGLE_TOOLTIP, TOGGLE_ZOOM_MODE, V_GRID_LINE } from "../actions/charts/actionType";

import { getTrendData, GetTrendDataRequest } from "../apis/TrendsApi";
import { Trend, TrendData, TrendDef } from "../models";
import { TrendDataApiFromJSON } from "../models/TrendDataApi";


export const PERIOD_EXTENSION = 2;

var x = new Date();
var currentTimeZoneOffsetInSeconds = x.getTimezoneOffset();


const initialState: ChartsState = {
    chart: {
      brush:{startIndex:0,endIndex:0},
      mode: { 
        zoom : false,
        tooltip:false,
        live : {active:false,
                timer:undefined
              }
      },
      is_loading_trends:true,
      grid_lines: {
        h: true,
        v: true
      },
      cfgRange: {
        from: Date.now()  - (60*60*1*1000),
        to: Date.now()
      }, 
      currRange: {
        from: Date.now() - ((PERIOD_EXTENSION)*(1*60*60*1000)+ (1*60*60*1000)),
        to: Date.now() + (PERIOD_EXTENSION*(1*60*60*1000))
      },
      refArea:{left:0,right:0},
      trends:[],
      data : [],
      lastUpdated:0,
    },
    rpanel_open:false
  }

const chartsReducer = (
    state: ChartsState = initialState,
    action: IChartAction
  ): ChartsState => {

    switch (action.type) {
        case DEFAULT_STATE:{
          return {
            ...state,
           chart: initialState.chart
          }
        }
        case TOGGLE_LIVE_MODE:{
          var currTimerange = state.chart.cfgRange.to - state.chart.cfgRange.from;
          //console.log(Date.now());
          //console.log(currTimerange);

         // var cfgTimeRange = state.chart.mode.live.active ? state.chart.cfgRange: {from: (Date.now() - (currTimerange)), to: Date.now()  } ;
          
         if (state.chart.mode.live.active){
            var cFrom =  state.chart.cfgRange.from - (PERIOD_EXTENSION*currTimerange);

            var cTo =  state.chart.cfgRange.to + (PERIOD_EXTENSION*currTimerange);
         }else{

          cTo = Date.now();
          cFrom = Date.now()-currTimerange;

         }

          //var trends = state.chart.trends.map((obj: any) => ({...obj}));
          
          //var DATA_SIZE = !state.chart.mode.live.active ? 800 : 4000;
          //console.log(DATA_SIZE);

          //var data1 = getData(timeRange.from,timeRange.to, DATA_SIZE, trends.filter(t => t.selected));
          


          return {
            ...state,
           chart: {brush:state.chart.brush,  lastUpdated:state.chart.lastUpdated, is_loading_trends : state.chart.is_loading_trends, trends:state.chart.trends, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip, live: {active:!state.chart.mode.live.active, timer:state.chart.mode.live.timer}, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:{from: cFrom, to:cTo}, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }
        case TOGGLE_TOOLTIP:{
         
          return {
            ...state,
           chart: {brush:state.chart.brush, lastUpdated:state.chart.lastUpdated, is_loading_trends : state.chart.is_loading_trends, trends:state.chart.trends, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:!state.chart.mode.tooltip, live: {active:state.chart.mode.live.active, timer:state.chart.mode.live.timer}, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }
        case TOGGLE_ZOOM_MODE:{
          return {
            ...state,
           chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated, is_loading_trends : state.chart.is_loading_trends,trends:state.chart.trends, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip, live:state.chart.mode.live, zoom:state.chart.mode.live.active ? false : !state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }

        case SET_DATE_RANGE:{
          
        var DATA_SIZE=4000;

        var range = state.chart.cfgRange.to - state.chart.cfgRange.from;
    
        if (range==0){
          range=1;
        }

        var cFrom =  state.chart.cfgRange.from - (PERIOD_EXTENSION*range);

        var cTo =  state.chart.cfgRange.to + (PERIOD_EXTENSION*range);

         // var trends = state.chart.trends.map((obj: any) => ({...obj}));

          //var data1 = getData(action.data.from, action.data.from + DATA_SIZE*range ,DATA_SIZE,  trends.filter(t => t.selected));

          return {
            ...state,
            chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : state.chart.is_loading_trends,trends:state.chart.trends, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:{from:state.chart.cfgRange.from, to:state.chart.cfgRange.to}, currRange:{from:cFrom, to: cTo}, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }
        
        
        case TOGGLE_RPANEL:{

            return {
              ...state,
              chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : state.chart.is_loading_trends,trends:state.chart.trends, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:!state.rpanel_open
            }
          }
          
          case V_GRID_LINE:{

            return {
              ...state,
              chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : state.chart.is_loading_trends,trends:state.chart.trends, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : {h : state.chart.grid_lines.h, v:action.data}}, rpanel_open:state.rpanel_open
            }
          }

          case H_GRID_LINE:{

            return {
              ...state,
              chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : state.chart.is_loading_trends,trends:state.chart.trends, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : {v : state.chart.grid_lines.v, h:action.data}}, rpanel_open:state.rpanel_open
            }
          }
        
        
        case ADD_SERIE:{

         var trd : ITrend[] = state.chart.trends.map((obj: ITrend) => ({...obj}));
          trd.forEach(element => {
            if (element.iD == action.data)
            {
              element.selected = true;  
            }
          });
          //console.log(trd);
          //console.log(state.chart.data);
          //var DATA_SIZE = state.chart.mode.live.active ? 800 : 4000;

        //  var data1 = getData(state.chart.currRange.from,state.chart.currRange.to, DATA_SIZE, trends.filter(t => t.selected));
          

          return {
            ...state,
            chart: {brush:state.chart.brush,lastUpdated:0,is_loading_trends : state.chart.is_loading_trends,trends:trd, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }
        case REMOVE_SERIE:{
          var data : any[] = [];
          var trds : ITrend[] = state.chart.trends.map((obj: ITrend) => ({...obj})); 
          if ((state.chart.data) && (state.chart.data.length>0)){
           data = state.chart.data.map((obj: any) => ({...obj}));
          }
         
         trds.forEach(element => {
            if (element.iD == action.data)
            {
              element.selected = false;
              if ((state.chart.data) && (state.chart.data.length>0)){
              data.forEach((dat: any) => {
                delete dat[element.iD];  
              });
            }
              
            }
          });
        

          return {
            ...state,
            chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : state.chart.is_loading_trends, trends:trds, refArea:state.chart.refArea, data : data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }
       /* case CHART_SIZE:{
          return {
            ...state,
            chart: {trends:state.chart.trends, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid : state.chart.grid}, rpanel_open:state.rpanel_open
          }
        }*/
        case APPEND_DATA:{
          data = state.chart.data.map((obj: any) => ({...obj}));
          data=data.slice(action.data.length, data.length);
          
          data.push(...action.data);

          return {
            ...state,
            chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : state.chart.is_loading_trends, trends:state.chart.trends, refArea:state.chart.refArea, data : data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }
        case SET_TIMER:{
          return {
            ...state,
            chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : state.chart.is_loading_trends,trends:state.chart.trends, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:{active:action.data?  true : false, timer:action.data}, zoom: action.data? false : state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }
        case AREA_REF:{
          return {
            ...state,
            chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : state.chart.is_loading_trends, trends:state.chart.trends, refArea:action.data, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:{active:state.chart.mode.live.active, timer:state.chart.mode.live.timer}, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }case SET_DATA:{
          var dat : ITrendData[]=[];

          var brushStartIndex=0;
          var brushEndIndex=0;

          if ((action.data) && (action.data.data) && (action.data.data.length > 0)){ 
            //brushEndIndex = action.data.data.length;
         //   console.log(action.data.data.length);
          //  console.log(state.chart.cfgRange.from);
           // console.log(state.chart.cfgRange.to);
          // console.log(action.data.data[0].timestamp);
           // console.log(action.data.data[action.data.data.length-1].timestamp);
            //for (var step = 0;  step < action.data.data.length; step++) {
              
         //   console.log(currentTimeZoneOffsetInSeconds);
            action.data.data.forEach((el:TrendData)=>{
            //  var el : TrendData = action.data.data[step];
              var ut = el.timestamp *1000 + el.timestampMs + currentTimeZoneOffsetInSeconds*1000;
              dat.push({...el, unixtime:ut});
              //brushStartIndex = brushStartIndex+1;
              //console.log(ut < state.chart.cfgRange.from)
             // if (step > 0){
             //   console.log(ut - (action.data.data[step-1].timestamp*1000 + action.data.data[step-1].timestampMs))
             // }
              if (el.timestamp *1000 + el.timestampMs  < state.chart.cfgRange.from - currentTimeZoneOffsetInSeconds*1000){
                brushStartIndex = brushStartIndex+1;
              }
              if (el.timestamp *1000 + el.timestampMs  < state.chart.cfgRange.to - currentTimeZoneOffsetInSeconds*1000){
                brushEndIndex = brushEndIndex+1;
              }
             // console.log(ut < state.chart.cfgRange.to)
             // if (ut < state.chart.cfgRange.to){
              //  console.log(ut);
              //console.log(state.chart.cfgRange.to)
               // brushEndIndex = brushEndIndex+1;
              //}else{
              //  console.log(ut);
              //  console.log(state.chart.cfgRange.to)
              //}
           // }
             })
          }
          /*var trends = state.chart.trends.map((obj: any) => ({...obj}));
          trends.forEach(element => {
            if (element.name == action.data)
            {
              element.selected = true;  
            }
          });
          var DATA_SIZE = state.chart.mode.live.active ? 800 : 4000;

         var range = Math.round((state.chart.currRange.to - state.chart.currRange.from)/DATA_SIZE);
    
         if (range==0){
          range=1;
         }
*/
          //var data1 = getData(action.data.from, action.data.from + DATA_SIZE*range ,100,  trends.filter(t => t.selected));
       //   console.log(brushStartIndex);
       //   console.log(brushEndIndex);
          
          return {
            ...state,
            chart: {brush:{startIndex:brushStartIndex, endIndex:brushEndIndex},lastUpdated:action.data.lastUpdated,is_loading_trends : state.chart.is_loading_trends,trends:state.chart.trends, refArea:state.chart.refArea, data : dat, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }case LOAD_DATA_STATE:{
          var dat : ITrendData[]=[];

          var brushStartIndex=0;
        var brushEndIndex=0;

          if (action.data.data.length > 0){ 
            action.data.data.forEach((el:TrendData)=>{
              var ut = el.timestamp *1000 + el.timestampMs;
           //AAA   dat.push({...el, unixtime:ut})
             // if (ut < state.chart.cfgRange.from){
             //   brushStartIndex=brushStartIndex+1;
             // }
             // if (ut < state.chart.cfgRange.to){
             //   brushEndIndex=brushEndIndex+1;
             // }
             })
          }

        //  console.log(brushStartIndex);
        //  console.log(brushEndIndex);
          return {
            ...state,
            chart: {brush:{startIndex:brushStartIndex, endIndex:brushEndIndex},lastUpdated:state.chart.lastUpdated,is_loading_trends : state.chart.is_loading_trends,trends:state.chart.trends, refArea:state.chart.refArea, data : dat, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }
        case SET_FROM_DATE:{
          return {
            ...state,
            chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : state.chart.is_loading_trends,trends:state.chart.trends, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:{from: action.data, to:state.chart.cfgRange.to}, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }
        case SET_TIMESTAMP_RANGE:{
          
          var range = action.data.to - action.data.from;
      
          if (range==0){
            range=1;
          }
  
         // var cFrom;
         // var cTo; 
          if (state.chart.mode.live.active){
          cFrom = action.data.from 
          cTo = action.data.to
            }else{
         cFrom = action.data.from - (PERIOD_EXTENSION*range);
          cTo =  action.data.to + (PERIOD_EXTENSION*range);
            }  
  
         

          return {
            ...state,
            chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : state.chart.is_loading_trends,trends:state.chart.trends, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:{from: action.data.from, to:action.data.to}, currRange:{from:cFrom, to:cTo}, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }
        case SET_TO_DATE:{
          return {
            ...state,
            chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : state.chart.is_loading_trends,trends:state.chart.trends, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:{from: state.chart.cfgRange.from, to:action.data}, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }
        case LOAD_TREND_LIST:{
         var trd : ITrend[] = action.data;
        
         trd.forEach((element: ITrend) => {
            var tmp : string =  element.symbol? element.symbol : element.iD.toString(); 
            tmp += element.unit? ' [' + element.unit + ']' : '';

            element.axislabel = tmp;
            element.disabled = false;
            //console.log(element);
           
          });
         // console.log(action.data);

          return {
            ...state,
            chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : false,trends:trd, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
          }
        }
        case DISABLE_TREND:{
          var trd : ITrend[] = state.chart.trends;
         
          trd.forEach((element: ITrend) => {
            if (element.iD == action.data){
             element.disabled = true;
            }
             //console.log(element);
            
           });
          // console.log(action.data);
 
           return {
             ...state,
             chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : false,trends:trd, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
           }
         }
         case ENABLE_TREND:{
          var trd : ITrend[] = state.chart.trends;
         
          trd.forEach((element: ITrend) => {
            if (element.iD == action.data){
             element.disabled = false;
            }
             //console.log(element);
            
           });
          // console.log(action.data);
 
           return {
             ...state,
             chart: {brush:state.chart.brush,lastUpdated:state.chart.lastUpdated,is_loading_trends : false,trends:trd, refArea:state.chart.refArea, data : state.chart.data, mode: {tooltip:state.chart.mode.tooltip,live:state.chart.mode.live, zoom:state.chart.mode.zoom}, cfgRange:state.chart.cfgRange, currRange:state.chart.currRange, grid_lines : state.chart.grid_lines}, rpanel_open:state.rpanel_open
           }
         }
 

       
    }
    return state
  }
  
  export default chartsReducer