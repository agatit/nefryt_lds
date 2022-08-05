import { CompactTable } from '@table-library/react-table-library/compact';
import * as React from "react";
import { shallowEqual, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { RootState } from "../..";
import { Layout } from "../../components/template/Layout";
import { EventsState } from "../Events/type";
import "./style.css";
import { useTheme } from '@table-library/react-table-library/theme';
import { getTheme } from '@table-library/react-table-library/baseline';
import { useSort } from '@table-library/react-table-library/sort';
import { getData } from "../../actions/events/actions";
import { Box, LinearProgress } from '@material-ui/core';
import { CartesianGrid, Legend, LineChart, ResponsiveContainer, XAxis } from 'recharts';
import { ChartsState } from '../Charts/type';




const DashboardPage: React.FC = () => {

  const reducer: EventsState = useSelector(
    (state: RootState) => state.eventsReducer,
    shallowEqual
  )

  const reducer1: ChartsState = useSelector(
    (state: RootState) => state.chartsReducer,
    shallowEqual
  )

  
  
  let data:any =reducer.table;

  const theme = useTheme([
    getTheme(),
    {
      BaseCell: `
      &:nth-of-type(1) {
        min-width: 35%;
        width: 35%;
      }
  
      &:nth-of-type(2), &:nth-of-type(3), &:nth-of-type(4) {
        min-width: 15%;
        width: 15%;
      }
  
      &:nth-of-type(5) {
        min-width: 20%;
        width: 20%;
      }
    `,
    },
  ]);
  
  const sort = useSort(
    data,
    {
      onChange: onSortChange,
    },
    {
      isServer: true,
      sortFns: {
       
      },
    },
  );
  
  function onSortChange(action:any, state:any) {
    const params = {
      sort: {
        sortKey: state.sortKey,
        reverse: state.reverse,
      },
    };
    getData(params);
  }
  
  const COLUMNS = [
    { label: 'Task', renderCell: (item:any) => item.name,resize: true, sort: { sortKey: 'TASK' } },
    {
      label: 'Deadline',
      renderCell: (item:any) =>
        item.deadline.toLocaleDateString('en-US', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
        }),
        resize: true,
        sort: { sortKey: 'Deadline' }
    },
    { label: 'Type', renderCell: (item:any) => item.type, resize: true, sort: { sortKey: 'TYPE' }},
    {
      label: 'Complete',
      renderCell: (item:any) => item.isComplete.toString(),
      resize: true,
    },
    { label: 'Tasks', renderCell: (item:any) => item.nodes?.length , resize: true, sort: { sortKey: 'Tasks' } },
   ];
  
  return (
    <Layout rPanel={{open:reducer1.rpanel_open, visible:true, 
              content:<></> 
            }} content={
    <div className={'root'}>
        <div id="dashboard-left">
        <>
              <Box sx={{ width: '100%', height:'10px'}}>
               
              {/*TrendsDataState.isPending &&  <LinearProgress />*/}
             </Box>
              
              <ResponsiveContainer width="100%" height="100%" >
              
                <LineChart
                  width={500}
                  height={300}
                  data={[]}
                  //onMouseDown={handleMouseDown}
                  //onMouseMove={handleMouseMove}
                  //onMouseUp={handleMouseUp}
                  
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  
                  <CartesianGrid horizontal={true} vertical={true} strokeDasharray="3 3" />
                  <XAxis dataKey="unixtime" padding={{ left: 20, right: 20 }}  />
                  
                 
                </LineChart>
                
               
              </ResponsiveContainer>

              </>
        </div>
        

        <div id="dashboard-right">
        <>
              <Box sx={{ width: '100%', height:'10px'}}>
               
              {/*TrendsDataState.isPending &&  <LinearProgress />*/}
             </Box>
              
              <ResponsiveContainer width="100%" height="100%" >
              
                <LineChart
                  width={500}
                  height={300}
                  data={[]}
                  //onMouseDown={handleMouseDown}
                  //onMouseMove={handleMouseMove}
                  //onMouseUp={handleMouseUp}
                  
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  
                  <CartesianGrid horizontal={true} vertical={true} strokeDasharray="3 3" />
                  <XAxis dataKey="unixtime" padding={{ left: 20, right: 20 }}  />
                  
                 
                </LineChart>
                
               
              </ResponsiveContainer>

              </>

        </div>
        <div id="dashboars-bottom">
          <CompactTable  data={data}    theme={theme} columns={COLUMNS} sort={sort}  /> 
        </div> 
    </div>
    }/>
  )
}

export {DashboardPage}