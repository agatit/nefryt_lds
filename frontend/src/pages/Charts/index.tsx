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



const ChartsPage: React.FC = () => {

  const dispatch :Dispatch = useDispatch();

  const reducer: ChartsState = useSelector(
    (state: RootState) => state.charts,
    shallowEqual
  )
  
  const navigate = useNavigate();
  //const { data, error, isLoading } = useListTrendsQuery();
  //console.log(data);
  //console.log(error);
  //console.log(isLoading);
const handleClick = async () => {
    
  
    
  navigate('/');
   
   
};


const handleToggleRightPanel  = (e: React.MouseEvent<HTMLElement>) => {
  //alert('aaa');
  dispatch(toggleRightPanel());
}


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