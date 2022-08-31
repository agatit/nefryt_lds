import React from 'react';
import {Accordion, AccordionDetails, AccordionSummary, Badge, Box, Button, Checkbox, IconButton, LinearProgress, makeStyles, Slider} from '@material-ui/core';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label, ReferenceArea, Brush, Surface, Symbols } from 'recharts';
import { CategoricalChartState } from "recharts/types/chart/generateCategoricalChart";
import { ChartsState, ITrend, ITrendData } from '../../features/charts/types';
import { shallowEqual, useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../app/store';
import moment from "moment";
import { straightLine } from "./StraightLine";
import { renderCusomizedLegend } from './legend';
import { useGetTrendDataQuery, useListTrendsQuery } from '../../store/trendApi';
import { areaRef, setBrushRange } from '../../features/charts/chartsSlice';
import { Dispatch } from '@reduxjs/toolkit';
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
      
    const SAMPLES_COUNT = reducer.chart.mode.live.active ? 1000 : 4000;
  
    useListTrendsQuery();

    var trdList :number[] = [];

    var trends :ITrend[]= reducer.chart.trends.map((obj: ITrend) => ({...obj}));
    const selTrd: ITrend[] =trends.filter((obj: ITrend) => obj.selected);
    const selTrdCount = selTrd.length;
    
    if (selTrd && (selTrd.length > 0)) {
      selTrd.forEach((obj: ITrend) => {
        trdList.push(obj.ID);
      });
    }

    useGetTrendDataQuery({trendIdList: trdList, begin: reducer.chart.currRange.from, end:reducer.chart.currRange.to, samples :  SAMPLES_COUNT});
    //trendIdList: number[];
    //begin: number;
    //end: number;
    //samples: number;

    //var TrendsDataState: QueryState={isFinished:false,isPending:false, lastUpdated:0};
    var TrendsDataState = {isPending:false};

   // var dat1 =reducer.chart.data;


    
    //var 

  /*  
dat1.forEach((element: ITrendData) => {
  var tmp:any={Timestamp: element.Timestamp, TimestampMs: element.Timestamp, unixtime: element.unixtime};

  activeTrends.forEach((trd:ITrend)=>{
    tmp[trd.ID] = element[trd.ID];
  });
  
  dat2.push(tmp);
  
  

});
*/
    const handleMouseDown = (e: CategoricalChartState) => {
        if (!e || !e.activeLabel) {
          return
        }
        
        dispatch(areaRef({left:e.activeLabel, right:0}))
      }

      const handleMouseMove = (e: CategoricalChartState) => {
        if (!e) {
          return
        }
      
        if (!reducer.chart.refArea.left) {
          return;
        }
      }

      const handleMouseUp = (e: any) => {
        if (!e || !e.activeLabel) {
          return
        }
      }

      const formatXAxis = (tickItem: any) => {
        //var tickItemA = tickItem/1000;
       // console.log(tickItem);
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
      
      const CustomizedLabelB = (props: any) => {
        return (
          <></>
        );
      };

      
    const formatYAxis = (item: any) => {
        return item.toLocaleString(undefined, { maximumFractionDigits: 2 })
    }

    
        const formatBrush = (unixTime: any, index: any)  => {
          //var unixTimeA = unixTime/1000;
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

        const formatValue = (value: any, index: any)  => {
            return value.toLocaleString(undefined, { maximumFractionDigits: 2 })
          }
          

         
//console.log(reducer.chart.trends);
          
      var trends :ITrend[]= reducer.chart.trends.map((obj: ITrend) => ({...obj}));
      const selectedTrends: ITrend[] =trends.filter((obj: ITrend) => obj.selected);
      const selectedTrendCount = selectedTrends.length;

     

  
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
                     stroke={trend.Color? trend.Color : '#8884d8'}
                     yAxisId={trend.ID}
                     dataKey={trend.ID}
                     axisLine={true}
                     tickLine={false}
                     tickCount={20}
                     domain={trend.autoscale? ['dataMin-0.1*dataMin', 'dataMax+0.1*dataMax'] : [trend.scale.min, trend.scale.max]}
                     label={<CustomizedLabelB />}
                     tickFormatter={formatYAxis}
                   >
                   <Label key={"YAXisLabel"+index}  fill={trend.Color? trend.Color : '#8884d8'}  dx={index % 2==0 ?40 : -20} angle={270} position='center' dy={30}>  
                     {trend.axislabel}
                   </Label>
                    </YAxis>
                   
                   ))}
                 

                  
                 {reducer.chart.mode.tooltip ? <Tooltip  labelFormatter={formatBrush} formatter={formatValue}  /> : <></>}
                
                 <Legend
                    verticalAlign="bottom"
                    height={36}
                    align="left"

              content={renderCusomizedLegend({selectedTrends: selectedTrends})}
            />
                   {selectedTrends.map((trend, index) => (
                     
                     <Line dot={<></>} key={"Line"+index} isAnimationActive={false} yAxisId={trend.ID} type={straightLine} dataKey={trend.ID} stroke={trend.Color? trend.Color : '#8884d8'} activeDot={{ r: 8 }} /> 
                      
                    ))}
                 
                  

                  {(selectedTrendCount>0) && reducer.chart.refArea.left && reducer.chart.refArea.right ? (
                     reducer.chart.trends.map((trend, index) => (
                    <ReferenceArea key={"ReferenceArea" + index} yAxisId={trend.ID} x1={reducer.chart.refArea.left} x2={reducer.chart.refArea.right} strokeOpacity={0.3} />
                    ))
                  ) : null
                
                }


       { !reducer.chart.mode.live.active?
    
              <><Brush dataKey="unixtime" startIndex={reducer.chart.brush.startIndex} endIndex={reducer.chart.brush.endIndex}
                        tickFormatter={formatBrush} onChange={p.onbrushchange} ></Brush>
                          
                        

                        </>  
                 : null }
                </LineChart>
                
               
              </ResponsiveContainer>

        
        </>

    )
}