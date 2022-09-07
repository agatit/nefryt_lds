import { Button } from "@material-ui/core";
import { Dispatch } from "@reduxjs/toolkit";
import * as React from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { RootState } from "../../app/store";
import { Layout } from "../../components/template/Layout";
import { setBrushRange, setTimer, setTimestampRange, toggleRightPanel } from "../../features/charts/chartsSlice";
import { ChartsState, ITrend, ITrendData } from "../../features/charts/types";
import { useGetTrendDataQuery, useListTrendsQuery } from "../../store/trendApi";
import { ChartsContent } from "./content";
import { ChartsRPanel } from "./rpanel";
import "./style.css";



const ChartsPage: React.FC = () => {
  useListTrendsQuery();

  const dispatch :Dispatch = useDispatch();

  const reducer: ChartsState = useSelector(
    (state: RootState) => state.charts,
    shallowEqual
  )
  
  const handleToggleRightPanel  = (e: React.MouseEvent<HTMLElement>) => {
    dispatch(toggleRightPanel());
  }

  var trdList :number[] = [];
  var trends = reducer.chart.trends.map((obj: any) => ({...obj}));
  const selectedTrends: any[] =trends.filter((obj: ITrend) => obj.selected);
  const selectedTrendsCount = selectedTrends.length;

  if (selectedTrendsCount > 0) {
    selectedTrends.forEach((obj: ITrend) => {
      if (obj.ID){
        trdList.push(obj.ID);
      }
    });
  }

  const SAMPLES_COUNT = reducer.chart.mode.live.active ? 1000 : 4000;

  useGetTrendDataQuery({trendIdList: trdList, begin: reducer.chart.currRange.from, end:reducer.chart.currRange.to, samples :  SAMPLES_COUNT});
    

  React.useEffect(() => {
    var interval: NodeJS.Timer | undefined;
    
    var selCount = selectedTrends.length;
    if (!reducer.chart.mode.live.timer && reducer.chart.mode.live.active && (selCount > 0)) {
      interval = setInterval(function() { 
        var from;
        var to;
        var currTimerange = reducer.chart.cfgRange.to - reducer.chart.cfgRange.from;
        to = Date.now() ;
        from = Date.now()-currTimerange;
        dispatch(setTimestampRange({from:from, to:to}));
      }, 3000);
      dispatch(setTimer(interval));
    }else if ((reducer.chart.mode.live.timer && !reducer.chart.mode.live.active)){
      clearInterval(reducer.chart.mode.live.timer);
      dispatch(setTimer(undefined));
    }
  }, [reducer])

  var data_range_from=0;
  var data_range_to=0;
  var brush_startIndex = 0;
  var brush_endIndex = 0;

  var trendData = reducer.chart.data;
  var activeTrendData : ITrendData[] = []; 
  const activeTrends: ITrend[] =reducer.chart.trends.filter((obj: ITrend) => obj.selected &&  !obj.disabled);
  trendData.forEach((element: ITrendData) => {
    var tmp:any={Timestamp: element.Timestamp, TimestampMs: element.Timestamp, unixtime: element.unixtime};
    activeTrends.forEach((trd:ITrend)=>{
      if (trd.ID){
        tmp[trd.ID] = element[trd.ID];
      }
    });
    activeTrendData.push(tmp);
  });

  const handleLayoutClick  = (e: React.MouseEvent<HTMLElement>) => {
    if ((data_range_from > 0) && (data_range_to>0)){
      dispatch(setBrushRange({from: data_range_from, to: data_range_to, startIndex: brush_startIndex, endIndex:brush_endIndex} ));
      data_range_from=0;
      data_range_to=0;
      brush_startIndex = 0;
      brush_endIndex = 0;
    }
  }

  const handleBrushChange = (a: any) => {
    var from;
    var to;
    data_range_from = activeTrendData[a.startIndex].unixtime;
    data_range_to = activeTrendData[a.endIndex].unixtime;
    brush_startIndex = a.startIndex;
    brush_endIndex = a.endIndex;
    from = activeTrendData[a.startIndex].unixtime; 
    to = activeTrendData[a.endIndex].unixtime;
  } 

  return (
    <Layout onmouseup={handleLayoutClick} content={<ChartsContent onbrushchange={handleBrushChange} data={activeTrendData}/>} rPanel={{
      enable: true,
      open: reducer.rpanel_open,
      content: <ChartsRPanel/>,
      handleDrawer: handleToggleRightPanel
    }}></Layout>    
  )
}

export {ChartsPage}