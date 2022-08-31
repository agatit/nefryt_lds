import { Button } from "@material-ui/core";
import { Dispatch } from "@reduxjs/toolkit";
import * as React from "react";
import ReactDOM from 'react-dom';
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { RootState } from "../../app/store";
import { Layout } from "../../components/template/Layout";
import { setTimer, setTimestampRange, toggleRightPanel } from "../../features/charts/chartsSlice";
import { ChartsState, ITrend } from "../../features/charts/types";
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