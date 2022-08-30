import { Button } from "@material-ui/core";
import { Dispatch } from "@reduxjs/toolkit";
import * as React from "react";
import ReactDOM from 'react-dom';
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { RootState } from "../../app/store";
import { Layout } from "../../components/template/Layout";
import { toggleRightPanel } from "../../features/charts/chartsSlice";
import { ChartsState } from "../../features/charts/types";
import { useListTrendsQuery } from "../../store/trendApi";
import { ChartsContent } from "./content";
import { ChartsRPanel } from "./rpanel";
import "./style.css";


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


import CustomSurface from "../../components/chart/CustomSurface";
import { ExpandMore} from '@material-ui/icons'
import Typography from '@mui/material/Typography';


var runLive : ForceRequestCallback;



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

function valuetext(value:any) {
  return `${value}°C`;
}

const ChartsPage: React.FC = () => {

  const [expanded, setExpanded] = React.useState('false');

  const handleSwitchOnlySelected = (event: any) => {
    dispatch(setOnlySelected(event.target.checked));
  }

  const handleChange = (panel: string) => (event: any, isExpanded: any) => {
   // console.log(event.target );
   // console.log(event.target.parentElement );
     console.log(event.target.classList.contains("changeAccordionState") );
    if ((event.target.classList.contains("changeAccordionState")) || ((event.target.parentElement) && (event.target.parentElement.classList.contains("changeAccordionState")))){
        setExpanded(isExpanded ? panel : 'false');
    }
  };

  var data_range_from=0;
  var data_range_to=0;
  var brush_startIndex = 0;
  var brush_endIndex = 0;

 
  // const queries = useSelector(getQueries) || [];
  // const entities = useSelector(getEntities) || [];

  // console.log(queries);
  // console.log(entities);

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
      //console.log('KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK');
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

const handleChangeTrend = (event: any) => {
  event.preventDefault();
  dispatch(changeTrend(event.target.name.replace('trd_', ''), event.target.checked));
  if (!event.target.checked){
    setExpanded('false');
  }
  
}
const toggleAutoscale = (event:any) => {
  dispatch(setAutoscale(event.target.name.replace('trd_manual_scale_', ''), !event.target.checked));
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
    <Layout content={<ChartsContent/>} rPanel={{
      enable: true,
      open: reducer.rpanel_open,
      content: <ChartsRPanel/>,
      handleDrawer: handleToggleRightPanel
    }}></Layout>    
  )
}

export {ChartsPage}