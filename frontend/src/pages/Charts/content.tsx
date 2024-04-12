import React from 'react';
import { Box, LinearProgress} from '@material-ui/core';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label, ReferenceArea, Brush } from 'recharts';
import { ChartsState, ITrend } from '../../features/charts/types';
import { shallowEqual, useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../app/store';
import moment from "moment";
import { straightLine } from "./StraightLine";
import { renderCusomizedLegend } from './legend';
import { disableTrend, enableTrend } from '../../features/charts/chartsSlice';
import { Dispatch } from '@reduxjs/toolkit';
import { CustomizedLabel } from './label';
import "./style.css";


interface BrushStartEndIndex {
  startIndex?: number;
  endIndex?: number;
}

type Props={
  data:any[];
  onbrushchange?:(React.FormEventHandler<SVGElement> & ((newIndex: BrushStartEndIndex) => void)) | undefined;
} 

export const ChartsContent: React.FC<Props> = (p) => { 
  const dispatch :Dispatch = useDispatch();
    
  const reducer: ChartsState = useSelector(
    (state: RootState) => state.charts,
    shallowEqual
  )    


  var trends :ITrend[]= reducer.chart.trends.map((obj: ITrend) => ({...obj}));
  const selectedTrends: ITrend[] =trends.filter((obj: ITrend) => obj.selected);
  const selectedTrendsCount = selectedTrends.length;
    
  const legendItemClick  = (item : ITrend) => {
    item.disabled? dispatch(enableTrend(item.ID)) :  dispatch(disableTrend(item.ID))
  }


  const formatXAxis = (tickItem: any) => {
    var range = reducer.chart.currRange.to-reducer.chart.currRange.from;
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
        
  const formatYAxis = (item: any) => {
    return item.toLocaleString(undefined, { maximumFractionDigits: 2 })
  }
  
  const formatBrush = (unixTime: any, index: any)  => {
    var range = reducer.chart.currRange.to-reducer.chart.currRange.from;
    var divHour = range /  (60*60*1000);
    var format:string='DD-MM-YYYY HH:mm:ss';      
    var ms :number = 0;    
    var tmpDate = new Date( unixTime );
    var tmpDateFormated =  moment(tmpDate).format(format);
        
    if (divHour <=1){
      ms = unixTime % 1000;
      tmpDateFormated = tmpDateFormated + '.' + ms;
    }
    return tmpDateFormated ;    
  }

  const formatTooltipValue = (value: any, index: any)  => {
    return value.toLocaleString(undefined, { maximumFractionDigits: 2 })
  }
                  
  return (
    <>
      <Box sx={{ width: '100%', height:'10px'}}>       
        {reducer.chart.is_loading_trends &&  <LinearProgress />}
      </Box>        
      <ResponsiveContainer width="100%" height="100%">  
        <LineChart
          width={500}
          height={300}
          data={p.data}         
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
                stroke={trend.Color? trend.Color : '#8884d8'}
                yAxisId={trend.ID}
                dataKey={trend.ID}
                axisLine={true}
                tickLine={false}
                tickCount={20}
                domain={trend.autoscale? ['dataMin-0.1*dataMin', 'dataMax+0.1*dataMax'] : [trend.scale.min, trend.scale.max]}
                label={<CustomizedLabel />}
                tickFormatter={formatYAxis}
              >
                <Label key={"YAXisLabel"+index}  fill={trend.Color? trend.Color : '#8884d8'}  dx={index % 2==0 ?40 : -20} angle={270} position='center' dy={30}>  
                  {trend.axislabel}
                </Label>
              </YAxis>         
            ))}
                          
            {reducer.chart.mode.tooltip ? <Tooltip  labelFormatter={formatBrush} formatter={formatTooltipValue}  /> : <></>}
              <Legend
                verticalAlign="bottom"
                height={36}
                align="left"
                content={renderCusomizedLegend({selectedTrends: selectedTrends, onItemClick : legendItemClick})}
              />
              {selectedTrends.map((trend, index) => (   
                <Line dot={<></>} key={"Line"+index} isAnimationActive={false} yAxisId={trend.ID} type={straightLine} dataKey={trend.ID} stroke={trend.Color? trend.Color : '#8884d8'} activeDot={{ r: 8 }} />        
              ))}
                  
              {!reducer.chart.mode.live.active?
                <>
                  <Brush dataKey="unixtime" startIndex={reducer.chart.brush.startIndex} endIndex={reducer.chart.brush.endIndex} tickFormatter={formatBrush} onChange={p.onbrushchange} ></Brush>
                </>  
                : null }
        </LineChart>         
      </ResponsiveContainer>
    </>
  )
}