 
 import React from 'react';
import { RootState } from '../../app/store';
import { ChartsState, ITrend } from '../../features/charts/types';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label, ReferenceArea, Brush, Surface, Symbols } from 'recharts';
import "./style.css";

  type ParamLegend ={
    selectedTrends : ITrend[],
    onItemClick : (item : ITrend) => void;
  }
  export const renderCusomizedLegend = (p :ParamLegend) => {
    return (
      <div className="customized-legend">
        {p.selectedTrends.map((entry: ITrend) => {
          const style = {
            marginRight: 10,
            color: entry.Color ? entry.Color : "#8884d8"
          };
          return (
            <span
              className="legend-item"
              onClick={() => {p.onItemClick(entry)}}
              style={style}
            >
              <Surface width={10} height={10} viewBox={{x:0, y:0, width:10, height:10}} >
                <Symbols cx={5} cy={5} type="circle" size={50} fill={entry.Color ? entry.Color:'#8884d8'} />
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
              <span>{entry.Symbol?entry.Symbol:entry.ID}</span>
            </span>
          );
        })}
      </div>
    );
  };