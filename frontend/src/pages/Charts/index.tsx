import { FormControl, FormControlLabel,  FormGroup,  FormHelperText,  FormLabel,  Stack, Switch, TextField } from "@mui/material";
import {Box, Button, Checkbox, LinearProgress, makeStyles} from '@material-ui/core';
import { DateTimePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { Dispatch, Store } from "@reduxjs/toolkit";
import * as React from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { RootState } from "../..";
import { appendData, setFromDate, setToDate,  toggleLiveMode, toggleZoomMode, areaRef, toggleTooltip, setTimer, changeTrend, setHorizontalLine, setVerticalLine, setData, setTrendList, setDateRange, setTimestampRange, enableTrend, disableTrend, setBrushRange, forceRefresh, clearTimer } from "../../actions/charts/actions";
import { Layout } from "../../components/template/Layout";
import { RightPanel } from "../../components/template/RightPanel";
import { ChartsState } from "./type";
import "./style.css";

import { PureComponent, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label, ReferenceArea, Brush, Surface, Symbols } from 'recharts';
import { verify } from "crypto";
import { usePreviousProps } from "@mui/utils";
import { gridColumnsTotalWidthSelector } from "@mui/x-data-grid";
import { CategoricalChartState } from "recharts/types/chart/generateCategoricalChart";
import { ITrend, ITrendData } from "../../components/chart/type";
import moment from "moment";

import { ForceRequestCallback, ForceRequestsCallback, useRequest, useRequests } from 'redux-query-react';
import { BASE_PATH, Configuration, TypedQueryConfig } from "../../runtime";
import { Method, Trend, TrendData, TrendDataFromJSON, TrendFromJSON } from "../../models";
import { listMethods } from "../../apis/MethodApi";
import { getTrendData, getTrendCurrentData, listTrendDefs, listTrends } from "../../apis/TrendsApi";
import store, {  getEntities, getQueries } from "../../store";
import { Entities, QueriesState, QueryConfig, QueryState, requestAsync, ResponseBody, updateEntities, UpdateStrategy } from "redux-query";
import { connectRequest } from 'redux-query-react';

import { QueryClient, useMutation, useQuery } from 'react-query';

import { CollectionsOutlined } from "@mui/icons-material";
import { request } from "http";
import { getLogger } from "react-query/types/core/logger";

import { straightLine } from "../../components/chart/StraightLine";

import { cancelQuery } from 'redux-query';

import { Slider, Rail, Handles, Tracks, Ticks } from 'react-compound-slider';
import {
  GetRailProps,
  GetHandleProps,
  GetTrackProps,
  SliderItem,
} from 'react-compound-slider';

interface SliderRailProps {
  getRailProps: GetRailProps;
}



// *******************************************************
// HANDLE COMPONENT
// *******************************************************
interface HandleProps {
  domain: number[];
  handle: SliderItem;
  getHandleProps: GetHandleProps;
}

export const Handle: React.FC<HandleProps> = ({
  domain: [min, max],
  handle: { id, value, percent },
  getHandleProps,
}) => {
  return (
    <>
      <div
        style={{
          top: `${percent}%`,
          position: 'absolute',
          transform: 'translate(-50%, -50%)',
          WebkitTapHighlightColor: 'rgba(0,0,0,0)',
          zIndex: 5,
          width: 42,
          height: 28,
          cursor: 'pointer',
          backgroundColor: 'none',
        }}
        {...getHandleProps(id)}
      />
      <div
        role="slider"
        aria-valuemin={min}
        aria-valuemax={max}
        aria-valuenow={value}
        style={{
          top: `${percent}%`,
          position: 'absolute',
          transform: 'translate(-50%, -50%)',
          zIndex: 2,
          width: 24,
          height: 24,
          borderRadius: '50%',
          boxShadow: '1px 1px 1px 1px rgba(0, 0, 0, 0.3)',
          backgroundColor: '#D7897E',
        }}
      />
    </>
  );
};

// *******************************************************
// TICK COMPONENT
// *******************************************************
interface TickProps {
  tick: SliderItem;
  format?: (val: number) => string;
}

export const Tick: React.FC<TickProps> = ({ tick, format = d => d }) => {
  return (
    <div>
      <div
        style={{
          position: 'absolute',
          marginTop: -0.5,
          marginLeft: 10,
          height: 1,
          width: 6,
          backgroundColor: 'rgb(200,200,200)',
          top: `${tick.percent}%`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          marginTop: -5,
          marginLeft: 20,
          fontSize: 10,
          top: `${tick.percent}%`,
        }}
      >
        {format(tick.value)}
      </div>
    </div>
  );
};


// *******************************************************
// TRACK COMPONENT
// *******************************************************
interface TrackProps {
  source: SliderItem;
  target: SliderItem;
  getTrackProps: GetTrackProps;
  disabled?: boolean;
}

export const Track: React.FC<TrackProps> = ({
  source,
  target,
  getTrackProps,
}) => {
  return (
    <div
      style={{
        position: 'absolute',
        zIndex: 1,
        backgroundColor: '#C55F4E',
        borderRadius: 7,
        cursor: 'pointer',
        width: 14,
        transform: 'translate(-50%, 0%)',
        top: `${source.percent}%`,
        height: `${target.percent - source.percent}%`,
      }}
      {...getTrackProps()}
    />
  );
};


var runLive : ForceRequestCallback;

const railOuterStyle = {
  position: 'absolute' as 'absolute',
  height: '100%',
  width: 42,
  transform: 'translate(-50%, 0%)',
  borderRadius: 7,
  cursor: 'pointer',
};

const railInnerStyle = {
  position: 'absolute' as 'absolute',
  height: '100%',
  width: 14,
  transform: 'translate(-50%, 0%)',
  borderRadius: 7,
  pointerEvents: 'none' as 'none',
  backgroundColor: 'rgb(155,155,155)',
};

export const SliderRail: React.FC<SliderRailProps> = ({ getRailProps }) => {
  return (
    <>
      <div style={railOuterStyle} {...getRailProps()} />
      <div style={railInnerStyle} />
    </>
  );
};

const useStyles  = makeStyles(theme => ({
  root:{
      display:'flex',  
    }, 
    appToolbar:{
      backgroundColor:'#0f5295',
      minHeight:50,
      maxHeight:50
    }, 
    appBar:{
      transition: theme.transitions.create(['margin', 'width'] ,{
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
      }),
    },
   
    menuButton:{
      marginRight: theme.spacing(2),
    },
    hide: {
      display:    'none',
    },
   
    drawerHeader:{
      display : 'flex',
      alignItems: 'center',
      padding: theme.spacing(0,1),
      ...theme.mixins.toolbar,  
    },
    sidebar:{
      backgroundColor: '#0f5295',
      minHeight:50,
      maxHeight:50,
    },
    sidebarTitle:{
      color: 'white',
      fontSize: '1rem',
      fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
      fontWeight : 400,
      lineHeight: 1.5,
      letterSpacing: '0.00938em',
      marginTop : 'auto',
      marginBottom : 'auto'
    },
    sidebarRightButton:{
      marginLeft: 'auto',
    },
    
}));

Configuration.basePath = 'http://192.168.1.231:8080';


const ChartsPage: React.FC = () => {

  var data_range_from=0;
  var data_range_to=0;
  var brush_startIndex = 0;
  var brush_endIndex = 0;

 
  const queries = useSelector(getQueries) || [];
  const entities = useSelector(getEntities) || [];

  console.log(queries);
  console.log(entities);

  const reducer: ChartsState = useSelector(
    (state: RootState) => state.chartsReducer,
    shallowEqual
  )


  var SAMPLES_COUNT;// = reducer.chart.mode.live.active ? 1000 : 4000;


  var trends :ITrend[]= reducer.chart.trends.map((obj: ITrend) => ({...obj}));
const selectedTrends: ITrend[] =trends.filter((obj: ITrend) => obj.selected);
const selectedTrendCount = selectedTrends.length;

var trdList :number[] = [];

if (selectedTrends && (selectedTrends.length > 0)) {
  selectedTrends.forEach((obj: ITrend) => {
    trdList.push(obj.iD);
  });
}



  var queryTrendsList = listTrends({
    queryKey: 'trends_list',
     transform: (data) => {
         return {
           trends_list: data,
         };
     },
     update: {
       trends_list: (oldValue: any, newValue: any) => {
         return (oldValue=newValue);
       },
     }
    }
  );

  var x = new Date();
  var currentTimeZoneOffsetInSeconds = x.getTimezoneOffset();
  var queryTrendsData;
  var queryTrendsLiveData;

 // if (reducer.chart.mode.live.active){
   // console.log('AAAAAA');
   // console.log(SAMPLES_COUNT);
    SAMPLES_COUNT=1000;

    var currTimerange = Math.round((reducer.chart.cfgRange.to - reducer.chart.cfgRange.from)/1000);
  //  console.log(currTimerange);

    queryTrendsLiveData = getTrendCurrentData({ trendIdList: trdList,period:currTimerange,samples: SAMPLES_COUNT},
       {
        //queryKey:'timestamp',
        transform:  (body:any, text:any) => {
          console.log(body);
          return {
            
            trends_live_data: body,
          }
        },
        update: {
          trends_live_data: (oldValue: any, newValue: any) => {
            
            return (newValue);
          },
        },
      });
      
 // }else{
   // console.log('BBBBBB');
   // SAMPLES_COUNT=4000;
   //console.log(trdList);
    if ( !reducer.chart.mode.live.active){
    queryTrendsData = getTrendData({trendIdList: trdList,
      begin: Math.round(reducer.chart.currRange.from /1000) - currentTimeZoneOffsetInSeconds, //1655796348,
      end: Math.round(reducer.chart.currRange.to /1000) - currentTimeZoneOffsetInSeconds,//1655804041,
      samples: SAMPLES_COUNT
    }, {
      
      transform:  (body:any, text:any) => {
        return {
          trends_data: body,
        }
      },
      update: {
        trends_data: (oldValue: any, newValue: any) => {
          return (newValue);
        },
      },
    });
  }
 // }


//    if ((reducer.chart.force_refresh) || (reducer.chart.mode.live.active)){
   //   console.log('force');
     // queryTrendsData.force =  reducer.chart.force_refresh || reducer.chart.mode.live.active;
    // console.log(reducer.chart.mode.live.active);
    if ( reducer.chart.mode.live.active){

     // console.log(entities);

      
//queries.forEach((element:any) => {
  //for (var i=0; i<(queries.length) ; i++){
  //cancelQuery(queries[i].url);
 // }

 //console.log(queries);
//});

//Object.keys(queries).forEach(function(key,index) {
//  console.log(key);
//  console.log(index) ;
//  cancelQuery(key);
//});



      
     queryTrendsLiveData.force = reducer.chart.mode.live.active || reducer.chart.force_refresh;

    // console.log(queryTrendsLiveData.url);
    }
    if (( !reducer.chart.mode.live.active) && queryTrendsData){
     queryTrendsData.force = reducer.chart.force_refresh;
    
    }
    

      //queryTrendsData.retry = true;
      //console.log(queryTrendsData.force);
     // queryTrendsData.retry = true;
     // run();
  //   }

  const dispatch :Dispatch = useDispatch();

  var TrendsDataState: QueryState={isFinished:false,isPending:false, lastUpdated:0};
  var run : ForceRequestsCallback;
  const styles = useStyles(); 
  //if (( !reducer.chart.mode.live.active) && queryTrendsData){
     [TrendsDataState, run] = useRequest(queryTrendsData);
  //}

  //connectRequest(queryTrendsLiveData);

   //const [{ isPendingAA }, reactToComment] = useMutation(queryTrendsLiveData);

  
   //var aa = useMutation(queryTrendsLiveData);

   //const aa = useSelector(getEntities) || [];
   //console.log(aa);
   var TrendsLiveDataState: QueryState;
   [ TrendsLiveDataState, runLive]= useRequest(queryTrendsLiveData);

  //if (reducer.chart.force_refresh) {
  //  TrendsLiveDataState = {isFinished:false,isPending:false, lastUpdated:0};
 //}

   const [TrendsListState] = useRequest(queryTrendsList);

   

   var dat1 =reducer.chart.data;

const activeTrends: any[] =trends.filter((obj: ITrend) => obj.selected &&  !obj.disabled);

var dat2:any[] = [];



dat1.forEach((element: ITrendData) => {
  var tmp:ITrendData={timestamp: element.timestamp, timestampMs: element.timestamp, unixtime: element.unixtime};

  activeTrends.forEach((trd:ITrend)=>{
    tmp[trd.iD] = element[trd.iD];
  });
  
  dat2.push(tmp);
  
  

});



   if ((!reducer.chart.mode.live.active)&& (TrendsDataState.isFinished) && (reducer.chart.lastUpdated != TrendsDataState.lastUpdated)){
     
    dispatch(setData(entities.trends_data, TrendsDataState.lastUpdated ? TrendsDataState.lastUpdated : 0 ));
     
     }
   //  console.log(entities);
   //  console.log(reducer.chart.lastUpdated);
   //  console.log(TrendsLiveDataState.lastUpdated);
   //  console.log(TrendsLiveDataState);
     if ((reducer.chart.mode.live.active)&&(TrendsLiveDataState.isFinished) && (reducer.chart.lastUpdated != TrendsLiveDataState.lastUpdated)){
       
      dispatch(setData(entities.trends_live_data, TrendsLiveDataState.lastUpdated ? TrendsLiveDataState.lastUpdated : 0 ));
       
       }

  useEffect(() => {
    //var runLive: 
    //alert('effect');
    if ((!reducer.chart.mode.live.active)&& (TrendsDataState.isFinished) && (reducer.chart.lastUpdated != TrendsDataState.lastUpdated)){
      dispatch(setData(entities.trends_data, TrendsDataState.lastUpdated ? TrendsDataState.lastUpdated : 0 ));
    }

    if ((reducer.chart.mode.live.active)&&(TrendsLiveDataState.isFinished) && (reducer.chart.lastUpdated != TrendsLiveDataState.lastUpdated)){
     
      dispatch(setData(entities.trends_live_data, TrendsLiveDataState.lastUpdated ? TrendsLiveDataState.lastUpdated : 0 ));
       
       }


  if ((reducer.chart.is_loading_trends) && (TrendsListState.isFinished) && (reducer.chart.trends.length==0)){
   
   
      dispatch(setTrendList(entities.trends_list));

  }





    var interval: NodeJS.Timer | undefined;
    
    var trends = reducer.chart.trends.map((obj: any) => ({...obj}));
    const selectedTrends: any[] =trends.filter((obj: ITrend) => obj.selected);

   var selCount = selectedTrends.length;
   //console.log('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');
   //console.log(!reducer.chart.mode.live.timer);
    if (!reducer.chart.mode.live.timer && reducer.chart.mode.live.active && (selCount > 0)) {
      console.log('KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK');
      interval = setInterval(function() { 
      
        var from;
        var to;
        var currTimerange = reducer.chart.cfgRange.to - reducer.chart.cfgRange.from;

          to = Date.now() ;
          from = Date.now()-currTimerange;
          //console.log(queryTrendsData);
        //  console.log('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC');
            console.log(runLive);
          runLive();
          
            //dispatch(setData(entities.trends_live_data, 0));
           //dispatch(setTimestampRange(from, to));
      }, 3000);
      dispatch(setTimer(interval));
    }else if ((reducer.chart.mode.live.timer && !reducer.chart.mode.live.active)){
      
      
      clearInterval(reducer.chart.mode.live.timer);

      dispatch(setTimer(undefined));
   }else if (reducer.chart.force_refresh){
    //console.log('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH');
    clearInterval(reducer.chart.mode.live.timer);
    dispatch(clearTimer());
   // dispatch(toggleLiveMode());
   // dispatch(toggleLiveMode());
   // runLive();
   }
  


  
}, [reducer])

  function changeDateFrom(this: any, newValue: number | null) {
    dispatch(setFromDate(newValue));
  }

  function changeDateTo(this: any, newValue: number | null) {
    dispatch(setToDate(newValue));
  }

  const changeDataRange = (e: React.MouseEvent<HTMLElement>) => {
    dispatch(setDateRange());
  }
  
 const handleMouseDown = (e: CategoricalChartState) => {
    if (!e || !e.activeLabel) {
      return
    }
    
    dispatch(areaRef({left:e.activeLabel, right:0}))
  }

  const handleMouseUp = (e: any) => {
  if (!e || !e.activeLabel) {
    return
  }
}

const handleMouseMove = (e: CategoricalChartState) => {
  if (!e) {
    return
  }

  if (!reducer.chart.refArea.left) {
    return;
  }
}


const changeBrush = (e: any) => {

}

const handleChangeTrend = (event: { target: { name: any; checked: any; }; }) => {

  dispatch(changeTrend(event.target.name.replace('trd_', ''), event.target.checked));
  
}



  const handleSwitch = (event: { target: { name: any; checked: any; }; }) => {
    if (event.target.name=='gl_horizontal'){
      dispatch(setHorizontalLine(event.target.checked));
    }else if (event.target.name=='gl_vertical'){
      dispatch(setVerticalLine(event.target.checked));
    }else if (event.target.name=='liveMode'){
      dispatch(toggleLiveMode());
    }else if (event.target.name=='zoomMode'){
      dispatch(toggleZoomMode());
    }else if (event.target.name=='tooltipMode'){
      dispatch(toggleTooltip());
    }else{

  }
  };

function zoom() {
  //console.log('zoom');
  //let { refAreaLeft, refAreaRight } = this.state;
  //const { data } = this.state;

 // if (refAreaLeft === refAreaRight || refAreaRight === '') {
 //   this.setState(() => ({
 //     refAreaLeft: '',
 //     refAreaRight: '',
  //  }));
  //  return;
 // }

  // xAxis domain
 // if (refAreaLeft > refAreaRight) [refAreaLeft, refAreaRight] = [refAreaRight, refAreaLeft];

  // yAxis domain
 // const [bottom, top] = getAxisYDomain(refAreaLeft, refAreaRight, 'cost', 1);
 // const [bottom2, top2] = getAxisYDomain(refAreaLeft, refAreaRight, 'impression', 50);

//  this.setState(() => ({
//    refAreaLeft: '',
//    refAreaRight: '',
//    data: data.slice(),
//    left: refAreaLeft,
//    right: refAreaRight,
//    bottom,
//    top,
//    bottom2,
//    top2,
 // }));
}

const handlemouseup  = (e: React.MouseEvent<HTMLElement>) => {
      if ((data_range_from > 0) && (data_range_to>0)){
        dispatch(setBrushRange(data_range_from, data_range_to, brush_startIndex, brush_endIndex ));
        data_range_from=0;
        data_range_to=0;
        brush_startIndex = 0;
        brush_endIndex = 0;
      }
}

const formatYAxis = (item: any) => {
  return item.toLocaleString(undefined, { maximumFractionDigits: 2 })
}

 const formatXAxis = (tickItem: any) => {
  var range = reducer.chart.currRange.to-reducer.chart.currRange.from;
  //var range = 1655804041 - 1655796348;
  var divMonth = range  /  (30*60*60*24*1000);
  var divWeek = range /  (7*60*60*24*1000);
  var divDay = range /  (60*60*24*1000);
  var divHour = range /  (60*60*1000);
  var divMinutes = range / (60*1000);

  var format:string='DD-MM-YYYY HH:mm:ss';  
  if (divMonth>=12){
    format='DD-MM-YYYY';  
  }else if (divWeek>=1){
    format='DD-MM HH:mm';
  }else if (divDay>=1){
    format='DD HH:mm';
  }else if (divHour>=1){
    format='HH:mm';
  }else if (divMinutes>10) {
    format='HH:mm:ss';
  }else{
    format='mm:ss';
  }

  var ms :number = 0;
 

  var tmp =  moment(tickItem).format(format);
  if (divMinutes <=10){
    ms = tickItem % 1000;
    tmp = tmp + '.' + ms;
 }
  return tmp;

}


const formatValue = (value: any, index: any)  => {
  return value.toLocaleString(undefined, { maximumFractionDigits: 2 })
}

const formatBrush = (unixTime: any, index: any)  => {
  var range = reducer.chart.currRange.to-reducer.chart.currRange.from;
  var divMonth = range  /  (30*60*60*24*1000);
  var divWeek = range /  (7*60*60*24*1000);
  var divDay = range /  (60*60*24*1000);
  var divHour = range /  (60*60*1000);
  var divMinutes = range / (60*1000);

  var format:string='DD-MM-YYYY HH:mm:ss';  


  var ms :number = 0;
 
  var aa = new Date( unixTime );
  var tmp =  moment(aa).format(format);

  if (divHour <=1){
    ms = unixTime % 1000;
    tmp = tmp + '.' + ms;
 }
  return tmp ;

}

var active:boolean=true;


const renderCusomizedLegend = (payload :any) => {
  return (
    <div className="customized-legend">
      {selectedTrends.map((entry: ITrend) => {
        
        const style = {
          marginRight: 10,
          color: entry.color ? entry.color : "#8884d8"
        };
        return (
          <span
            className="legend-item"
            onClick={() => { entry.disabled? dispatch(enableTrend(entry.iD)) :  dispatch(disableTrend(entry.iD))}} //this.handleClick(dataKey)}
            style={style}
          >
            <Surface width={10} height={10} viewBox={{x:0, y:0, width:10, height:10}} >
              <Symbols cx={5} cy={5} type="circle" size={50} fill={entry.color ? entry.color:'#8884d8'} />
              { entry.disabled && (
                <Symbols
                  cx={5}
                  cy={5}
                  type="circle"
                  size={25}
                  fill={"#FFF"}
                />
              )}
            </Surface>
            <span>{entry.symbol?entry.symbol:entry.iD}</span>
          </span>
        );
      })}
    </div>
  );
};



if ((dat1) && (dat1.length>0)){

}


const sliderStyle: React.CSSProperties = {
  position: 'relative',
  height: '400px',
  marginLeft: '45%',
  touchAction: 'none',
};

const domain = [100, 500];
const defaultValues = [150, 300, 400, 450];
const  values = defaultValues.slice();


//const makeDraggable :React.ReactEventHandler<SVGRectElement> = {  (evt) => {

  const makeDraggable:React.ReactEventHandler<SVGRectElement> = (evt) => {
    //alert();
    //console.log(evt);
    var svg = evt.target;

  //alert('hhh');
  svg.addEventListener('mousedown', startDrag);
  svg.addEventListener('mousemove', drag);
  svg.addEventListener('mouseup', endDrag);
  svg.addEventListener('mouseleave', endDrag);
  function startDrag(evt:any) {
    alert('aaaa');
  }
  function drag(evt:any) {
  }
  function endDrag(evt:any) {
  }
}

const CustomizedLabelB = (props: any) => {
  return (
    <rect width="30" height="30" x="65" y="380"  />
  /*  <Slider
          vertical
          mode={1}
          step={5}
          domain={domain}
          rootStyle={sliderStyle}
          component="rect"
          //onUpdate={}
          //onChange={}
          values={values}
        >
          <Rail>
            {({ getRailProps }) => <SliderRail getRailProps={getRailProps} />}
          </Rail>
          <Handles>
            {({ handles, getHandleProps }) => (
              <div className="slider-handles">
                {handles.map(handle => (
                  <Handle
                    key={handle.id}
                    handle={handle}
                    domain={domain}
                    getHandleProps={getHandleProps}
                  />
                ))}
              </div>
            )}
          </Handles>
          <Tracks left={false} right={false}>
            {({ tracks, getTrackProps }) => (
              <div className="slider-tracks">
                {tracks.map(({ id, source, target }) => (
                  <Track
                    key={id}
                    source={source}
                    target={target}
                    getTrackProps={getTrackProps}
                  />
                ))}
              </div>
            )}
          </Tracks>
          <Ticks count={10}>
            {({ ticks }) => (
              <div className="slider-ticks">
                {ticks.map(tick => (
                  <Tick key={tick.id} tick={tick} />
                ))}
              </div>
            )}
          </Ticks>
        </Slider>

                */ 
  );
};

  return (   
    <Layout onmouseup={handlemouseup}  rPanel={{open:reducer.rpanel_open, visible:true, 
              content:
              <> 
              
               <LocalizationProvider dateAdapter={AdapterDateFns}> 
                <Stack spacing={3}>
                  <FormControlLabel
                    control={
                      <Switch checked={reducer.chart.mode.live.active} onChange={handleSwitch} name="liveMode" />
                    }
                    label="Dane bieżące"
                  />
    
                  <DateTimePicker
                    renderInput={(params) => <TextField {...params} />}
                    label="Zakres od"
                    value={reducer.chart.cfgRange.from}
                    ampm={false}
                    onChange={(newValue) => {
                      changeDateFrom(newValue);
                    }}
                    //views={['hours', 'minutes', 'seconds']} 
                    inputFormat="dd-MM-yyyy HH:mm:ss"
                    mask="__ -__-____ __:__:__"
                  />
                  <DateTimePicker
                    renderInput={(params) => <TextField {...params} />}
                    label="Zakres do"
                    value={reducer.chart.cfgRange.to}
                    ampm={false}
                    onChange={(newValue) => {
                      changeDateTo(newValue);
                    }}
                    //views={['hours', 'minutes', 'seconds']} 
                    inputFormat="dd-MM-yyyy HH:mm:ss"
                    mask="__ -__-____ __:__:__"
                  />
                   <Button disabled={reducer.chart.mode.live.active} onClick={changeDataRange} variant="contained">Ustaw zakres dat</Button>
                  
                    
                 

                  <div style={{border: 'solid 1px white' , maxHeight: 250, overflow:'auto'}}>
                    <FormControl sx={{ m: 3 }} component="fieldset" variant="standard">
                      <FormLabel component="legend">Wybór trendów (Wybrano: {selectedTrendCount})</FormLabel>
                      <FormGroup>
                          {reducer.chart.trends.map((trend : ITrend, index) => (
                            <FormControlLabel key={index}
                              control={
                              <Checkbox key={trend.iD } checked={trend.selected ? trend.selected : false} onChange={handleChangeTrend} name={"trd_" + trend.iD.toLocaleString()} />
                           }
                              label={trend.name}
                            />
                          ))
                          }
                      </FormGroup>
                      <FormHelperText> </FormHelperText>
                    </FormControl>
                  </div>

                  <div style={{border: 'solid 1px white'}}>      
                    <FormControl component="fieldset" variant="standard">
                      <FormLabel component="legend">Parametry wykresów</FormLabel>
                      <FormGroup>
                       { /*<FormControlLabel
                          control={
                           <Switch checked={reducer.chart.mode.zoom} disabled={reducer.chart.mode.live.active? true : false}   onChange={handleSwitch} name="zoomMode" />
                          }
                          label="Tryb zoom"
                        />
                        */
                       }
                        <FormControlLabel
                          control={
                           <Switch checked={reducer.chart.mode.tooltip} onChange={handleSwitch} name="tooltipMode" />
                          }
                          label="Pokazuj wartości"
                        />
                        <FormControlLabel
                          control={
                            <Switch checked={reducer.chart.grid_lines.h} onChange={handleSwitch} name="gl_horizontal" />
                          }
                          label="Poziome linie siatki"
                        />
                        <FormControlLabel
                          control={
                            <Switch checked={reducer.chart.grid_lines.v} onChange={handleSwitch} name="gl_vertical" />
                          }
                          label="Pionowe linie siatki"
                        />
                      </FormGroup>
                      <FormHelperText></FormHelperText>
                    </FormControl>
                  </div>
                </Stack>
              </LocalizationProvider>
              </> 
            }} content={ 
              <>
              <Box sx={{ width: '100%', height:'10px'}}>
               
              {TrendsDataState.isPending &&  <LinearProgress />}
             </Box>
              
              <ResponsiveContainer width="100%" height="100%" >
              
                <LineChart
                  width={500}
                  height={300}
                  data={dat2}
                  onMouseDown={handleMouseDown}
                  onMouseMove={handleMouseMove}
                  // eslint-disable-next-line react/jsx-no-bind
                  onMouseUp={handleMouseUp}

                   
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  
                  <CartesianGrid horizontal={reducer.chart.grid_lines.h} vertical={reducer.chart.grid_lines.v} strokeDasharray="3 3" />
                  <XAxis dataKey="unixtime" padding={{ left: 20, right: 20 }} tickFormatter =  {formatXAxis} />
                  {selectedTrends.map((trend, index) => (
                     
                     <YAxis key={"YAxis" + index}
                     orientation= {index % 2==0 ?  "left":"right"}
                     stroke={trend.color? trend.color : '#8884d8'}
                     yAxisId={trend.iD}
                     dataKey={trend.iD}
                     axisLine={true}
                     tickLine={false}
                     tickCount={20}
                     domain={['dataMin-0.1*dataMin', 'dataMax+0.1*dataMax']}
                     //label={<CustomizedLabelB />}
                     tickFormatter={formatYAxis}
                   >
                   <Label key={"YAXisLabel"+index}  fill={trend.color? trend.color : '#8884d8'}  dx={index % 2==0 ?40 : -20} angle={270} position='center' dy={30}>  
                     {trend.axislabel}
                   </Label>
                    </YAxis>
                   
                   ))}
                 

                  
                 {reducer.chart.mode.tooltip ? <Tooltip  labelFormatter={formatBrush} formatter={formatValue}  /> : <></>}
                
                 <Legend
              verticalAlign="bottom"
              height={36}
              align="left"

              content={renderCusomizedLegend}
            />
                   {selectedTrends.map((trend, index) => (
                     
                     <Line dot={<></>} key={"Line"+index} isAnimationActive={false} yAxisId={trend.iD} type={straightLine} dataKey={trend.iD} stroke={trend.color? trend.color : '#8884d8'} activeDot={{ r: 8 }} /> 
                      
                    ))}
                 
                  

                  {(selectedTrendCount>0) && reducer.chart.refArea.left && reducer.chart.refArea.right ? (
                     reducer.chart.trends.map((trend, index) => (
                    <ReferenceArea key={"ReferenceArea" + index} yAxisId={trend.iD} x1={reducer.chart.refArea.left} x2={reducer.chart.refArea.right} strokeOpacity={0.3} />
                    ))
                  ) : null
                
                }


       { !reducer.chart.mode.live.active?
    
              <><Brush dataKey="unixtime" startIndex={reducer.chart.brush.startIndex} endIndex={reducer.chart.brush.endIndex}
                        tickFormatter={formatBrush} onChange={(a: any) => {

                          var from;
                          var to;
                          data_range_from = dat2[a.startIndex].unixtime;
                          data_range_to = dat2[a.endIndex].unixtime;
                          brush_startIndex = a.startIndex;
                          brush_endIndex = a.endIndex;

                          from = dat2[a.startIndex].unixtime; //- range * (Math.round(0.9*DATA_SIZE/2));
                          to = dat2[a.endIndex].unixtime;

                          
                        } } />

                        </>  
                 : null }
                </LineChart>
                
               
              </ResponsiveContainer>
              </>
      }/>
  )
}

export {ChartsPage}


function getIntroOfPage(label: any): React.ReactNode {
  throw new Error("Function not implemented.");
}

