import { FormControl, FormControlLabel,  FormGroup,  FormHelperText,  FormLabel,  Stack, Switch, TextField } from "@mui/material";
import {Box, Button, Checkbox, LinearProgress, makeStyles} from '@material-ui/core';
import { DateTimePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { Dispatch, Store } from "@reduxjs/toolkit";
import * as React from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { RootState } from "../..";
import { appendData, setFromDate, setToDate,  toggleLiveMode, toggleZoomMode, areaRef, toggleTooltip, setTimer, changeTrend, setHorizontalLine, setVerticalLine, setData, loadData, setTrendList, setDateRange, setTimestampRange } from "../../actions/charts/actions";
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
import { ITrend } from "../../components/chart/type";
import moment from "moment";

import { useRequest, useRequests } from 'redux-query-react';
import { BASE_PATH, Configuration, TypedQueryConfig } from "../../runtime";
import { Method, Trend, TrendData, TrendDataFromJSON, TrendFromJSON } from "../../models";
import { listMethods } from "../../apis/MethodApi";
import { getTrendData, listTrendDefs, listTrends } from "../../apis/TrendsApi";
import store, {  getEntities, getQueries } from "../../store";
import { Entities, QueriesState, QueryConfig, QueryState, requestAsync, ResponseBody, updateEntities, UpdateStrategy } from "redux-query";
import { connectRequest } from 'redux-query-react';

import { QueryClient, useMutation, useQuery } from 'react-query';

import { CollectionsOutlined } from "@mui/icons-material";
import { request } from "http";
import { getLogger } from "react-query/types/core/logger";


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

  const queries = useSelector(getQueries) || [];
  const entities = useSelector(getEntities) || [];

  const reducer: ChartsState = useSelector(
    (state: RootState) => state.chartsReducer,
    shallowEqual
  )


  const SAMPLES_COUNT = reducer.chart.mode.live.active ? 1000 : 4000;


  var trends :ITrend[]= reducer.chart.trends.map((obj: ITrend) => ({...obj}));
const selectedTrends: ITrend[] =trends.filter((obj: ITrend) => obj.selected);
const selectedTrendCount = selectedTrends.length;

var trdList :number[] = [];

if (selectedTrends && (selectedTrends.length > 0)) {
  selectedTrends.forEach((obj: ITrend) => {
    trdList.push(obj.iD);
  });
}//else{
  //trdList.push();
//}


  var queryTrendsList = listTrends({
    queryKey: 'trends_list',
     transform: (data) => {
      // console.log(data);
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

  //reducer.chart.currRange.to-reducer.chart.currRange.from
  //var range = Math.round(reducer.chart.currRange.to /1000) - Math.round(reducer.chart.currRange.from /1000);

  var x = new Date();
 var currentTimeZoneOffsetInSeconds = x.getTimezoneOffset();

  var queryTrendsData = getTrendData({trendIdList: trdList,
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

  const dispatch :Dispatch = useDispatch();

  const styles = useStyles(); 

   const [ TrendsDataState, run] = useRequest(queryTrendsData);

   const [TrendsListState] = useRequest(queryTrendsList);
 
   //console.log(TrendsDataState);
   //console.log(queryTrendsData);
   //console.log(entities.trends_data);

   if ((TrendsDataState.isFinished) && (reducer.chart.lastUpdated!=0) && (reducer.chart.lastUpdated != TrendsDataState.lastUpdated)){
       //console.log(entities.trends_data);
       dispatch(setData(entities.trends_data, TrendsDataState.lastUpdated ? TrendsDataState.lastUpdated : 0 ));
     }
  useEffect(() => {
    //console.log(reducer.chart.lastUpdated);
    //console.log(TrendsDataState.lastUpdated); 

    //console.log(TrendsDataState);
    //console.log(queryTrendsData);   
    if ((TrendsDataState.isFinished) && (reducer.chart.lastUpdated != TrendsDataState.lastUpdated)){
      //console.log(entities.trends_data);
      dispatch(setData(entities.trends_data, TrendsDataState.lastUpdated ? TrendsDataState.lastUpdated : 0 ));
    }

  if ((reducer.chart.is_loading_trends) && (TrendsListState.isFinished)){
    if (queries.trends_list.isFinished){
      dispatch(setTrendList(entities.trends_list));
    }
  }



    var interval: NodeJS.Timer | undefined;
    
    var trends = reducer.chart.trends.map((obj: any) => ({...obj}));
    const selectedTrends: any[] =trends.filter((obj: ITrend) => obj.selected);

   var selCount = selectedTrends.length;
    if (!reducer.chart.mode.live.timer && reducer.chart.mode.live.active && (selCount > 0)) {
      interval = setInterval(function() { 
      
        var from;
        var to;
        var currTimerange = reducer.chart.cfgRange.to - reducer.chart.cfgRange.from;

          to = Date.now() ;
          from = Date.now()-currTimerange;
            
            dispatch(setTimestampRange(from, to));
      }, 3000);
      dispatch(setTimer(interval));
    }else if (reducer.chart.mode.live.timer && !reducer.chart.mode.live.active){
      clearInterval(reducer.chart.mode.live.timer);
      dispatch(setTimer(undefined));
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
//const handleMouseUp = (e: CategoricalChartState) => {
  const handleMouseUp = (e: any) => {
 // console.log('GGGGGGGGGGG');
 // console.log(e);
  if (!e || !e.activeLabel) {
    return
  }
  //zoom();

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


  var dat =reducer.chart.data;

  if ((dat) && (dat.length>0)){
   var dat2 = dat.map((obj: any) => ({...obj}));
    //console.log(dat2.length);
    //console.log(dat2);
  }


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
  //console.log(e.target);
 // if ((e) && (e.target) && ((e.target as Element).classList.contains('recharts-brush-slide'))){
      if ((data_range_from > 0) && (data_range_to>0)){
        dispatch(setTimestampRange(data_range_from, data_range_to));
        data_range_from=0;
        data_range_to=0;
      }
 // }
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
//console.log(divMinutes);
  if (divMinutes <=10){
    ms = tickItem % 1000;
    tmp = tmp + '.' + ms;
 }
 //tmp = tickItem;
  return tmp;

}

const formatBrush = (unixTime: any, index: any)  => {
  var range = reducer.chart.currRange.to-reducer.chart.currRange.from;
  //var range = 1655804041 - 1655796348;

  var divMonth = range  /  (30*60*60*24*1000);
  var divWeek = range /  (7*60*60*24*1000);
  var divDay = range /  (60*60*24*1000);
  var divHour = range /  (60*60*1000);
  var divMinutes = range / (60*1000);

  var format:string='DD-MM-YYYY HH:mm:ss';  


  var ms :number = 0;
 

  var tmp =  moment(unixTime).format(format);

  if (divHour <=1){
    ms = unixTime % 1000;
    tmp = tmp + '.' + ms;
 }
 //tmp = tickItem;
  return tmp ;

}

var active:boolean=true;
const renderCusomizedLegend = (payload :any) => {
  return (
    <div className="customized-legend">
      {selectedTrends.map((entry: ITrend) => {
        
        //const active = true; //_.includes(this.state.disabled, dataKey);
        const style = {
          marginRight: 10,
          color: entry.color ? entry.color : "#8884d8"
        };
      console.log(active);
        return (
          <span
            className="legend-item"
            onClick={() => { console.log('change acvtive')}} //this.handleClick(dataKey)}
            style={style}
          >
            <Surface width={10} height={10} viewBox={{x:0, y:0, width:10, height:10}} >
              <Symbols cx={5} cy={5} type="circle" size={50} fill={entry.color ? entry.color:'#8884d8'} />
              {false && (
                <Symbols
                  cx={5}
                  cy={5}
                  type="circle"
                  size={25}
                  fill={"#FFF"}
                />
              )}
            </Surface>
            <span>{entry.symbol}</span>
          </span>
        );
      })}
    </div>
  );
};


//{=> moment(unixTime).format("DD-MM-YYYY HH:mm:ss")} 

//console.log(Math.round(dat.length * 0.45));
//console.log(Math.round(dat.length * 0.55));
//console.log(dat);
if ((dat) && (dat.length>0)){


//console.log(dat[Math.round(dat.length * 0.45)].timestamp);
//console.log(dat[Math.round(dat.length * 0.55)].timestamp);
}


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
                        <FormControlLabel
                          control={
                           <Switch checked={reducer.chart.mode.zoom} disabled={reducer.chart.mode.live.active? true : false}   onChange={handleSwitch} name="zoomMode" />
                          }
                          label="Tryb zoom"
                        />
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
                  data={dat}
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
                     domain={['dataMin-0.1*dataMin', 'dataMax+0.1*dataMax']}
                     tickFormatter={formatYAxis}
                   >
                   <Label key={"YAXisLabel"+index} fill={trend.color? trend.color : '#8884d8'}  dx={index % 2==0 ?45 : -30} angle={270} position='center' dy={30}>  
                     {trend.axislabel}
                   </Label>
                    </YAxis>
                   
                   ))}
                 

                  
                 {reducer.chart.mode.tooltip ? <Tooltip labelFormatter={formatBrush} /> : <></>}
                
                 <Legend
              verticalAlign="bottom"
              height={36}
              align="left"
              //payload={_.toPairs(this.state.chartColors).map(pair => ({
              //  dataKey: pair[0],
              //  color: pair[1]
              //}))}
              content={renderCusomizedLegend}
            />
                   {selectedTrends.map((trend, index) => (
                     
                     <Line dot={<></>} key={"Line"+index} isAnimationActive={false} yAxisId={trend.iD} type="monotone" dataKey={trend.iD} stroke={trend.color? trend.color : '#8884d8'} activeDot={{ r: 8 }} /> 
                      
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
                          //setTimeout(()=>{  
                          var from;
                          var to;
                          data_range_from = dat[a.startIndex].unixtime;
                          data_range_to = dat[a.endIndex].unixtime;

                          from = dat[a.startIndex].unixtime; //- range * (Math.round(0.9*DATA_SIZE/2));
                          to = dat[a.endIndex].unixtime;

                          
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


