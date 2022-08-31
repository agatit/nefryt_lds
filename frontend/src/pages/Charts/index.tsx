import { Button } from "@material-ui/core";
import { Dispatch } from "@reduxjs/toolkit";
import * as React from "react";
import ReactDOM from 'react-dom';
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { RootState } from "../../app/store";
import { Layout } from "../../components/template/Layout";
import { setBrushRange, setTimer, setTimestampRange, toggleRightPanel } from "../../features/charts/chartsSlice";
import { ChartsState, ITrend, ITrendData } from "../../features/charts/types";
import { useListTrendsQuery } from "../../store/trendApi";
import { ChartsContent } from "./content";
import { ChartsRPanel } from "./rpanel";
import "./style.css";



const ChartsPage: React.FC = () => {

  const dispatch :Dispatch = useDispatch();

  const reducer: ChartsState = useSelector(
    (state: RootState) => state.charts,
    shallowEqual
  )
  
  const handleToggleRightPanel  = (e: React.MouseEvent<HTMLElement>) => {
    dispatch(toggleRightPanel());
  }


  React.useEffect(() => {
    //var runLive: 
    //alert('effect');
    //if ((!reducer.chart.mode.live.active)&& (TrendsDataState.isFinished) && (reducer.chart.lastUpdated != TrendsDataState.lastUpdated)){
    //  dispatch(setData(entities.trends_data, TrendsDataState.lastUpdated ? TrendsDataState.lastUpdated : 0 ));
    //}
    //if ((reducer.chart.mode.live.active)&&(TrendsLiveDataState.isFinished) && (reducer.chart.lastUpdated != TrendsLiveDataState.lastUpdated)){ 
    //   dispatch(setData(entities.trends_live_data, TrendsLiveDataState.lastUpdated ? TrendsLiveDataState.lastUpdated : 0 ));   
    //}
    //if ((reducer.chart.is_loading_trends) && (TrendsListState.isFinished) && (reducer.chart.trends.length==0)){ 
    //  dispatch(setTrendList(entities.trends_list));
    //}
    var interval: NodeJS.Timer | undefined;
    
    var trends = reducer.chart.trends.map((obj: any) => ({...obj}));
    const selectedTrends: any[] =trends.filter((obj: ITrend) => obj.selected);

    var selCount = selectedTrends.length;
    if (!reducer.chart.mode.live.timer && reducer.chart.mode.live.active && (selCount > 0)) {
        interval = setInterval(function() { 
          var from;
          var to;
          var currTimerange = reducer.chart.cfgRange.to - reducer.chart.cfgRange.from;
         // console.log(currTimerange);
          to = Date.now() ;
          from = Date.now()-currTimerange;
          dispatch(setTimestampRange({from:from, to:to}));
          //runLive();
        }, 3000);
        dispatch(setTimer(interval));
    }else if ((reducer.chart.mode.live.timer && !reducer.chart.mode.live.active)){
        clearInterval(reducer.chart.mode.live.timer);
        dispatch(setTimer(undefined));
    }
    //else if (reducer.chart.force_refresh){
    //    clearInterval(reducer.chart.mode.live.timer);
    //    dispatch(clearTimer());
    //}

  }, [reducer])

 /* const handlemouseup = (e: any) => {
    if (!e || !e.activeLabel) {
      return
    }
  }
  */

  var data_range_from=0;
  var data_range_to=0;
  var brush_startIndex = 0;
  var brush_endIndex = 0;

  var dat1 =reducer.chart.data;

  
  var dat2 : any[] = []; 
  const activeTrends: any[] =reducer.chart.trends.filter((obj: ITrend) => obj.selected &&  !obj.disabled);

  
dat1.forEach((element: ITrendData) => {
var tmp:any={Timestamp: element.Timestamp, TimestampMs: element.Timestamp, unixtime: element.unixtime};

activeTrends.forEach((trd:ITrend)=>{
  tmp[trd.ID] = element[trd.ID];
});

dat2.push(tmp);



});


  const handlemouseup  = (e: React.MouseEvent<HTMLElement>) => {
    //alert('AAAAAAAAAAAAAAAAAAAAA');
    //console.log(data_range_from);
    if ((data_range_from > 0) && (data_range_to>0)){
      
      dispatch(setBrushRange({from: data_range_from, to: data_range_to, startIndex: brush_startIndex, endIndex:brush_endIndex} ));
      data_range_from=0;
      data_range_to=0;
      brush_startIndex = 0;
      brush_endIndex = 0;
    }
}

  const handlebrushchange = (a: any) => {

    var from;
    var to;
    data_range_from = dat2[a.startIndex].unixtime;
    data_range_to = dat2[a.endIndex].unixtime;
    brush_startIndex = a.startIndex;
    brush_endIndex = a.endIndex;

    from = dat2[a.startIndex].unixtime; //- range * (Math.round(0.9*DATA_SIZE/2));
    to = dat2[a.endIndex].unixtime;

    
  } 


  return (
    <Layout onmouseup={handlemouseup} content={<ChartsContent onbrushchange={handlebrushchange} data={dat2}/>} rPanel={{
      enable: true,
      open: reducer.rpanel_open,
      content: <ChartsRPanel/>,
      handleDrawer: handleToggleRightPanel
    }}></Layout>    
  )
}

export {ChartsPage}