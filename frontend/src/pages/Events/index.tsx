import * as React from "react";
import { Link } from "react-router-dom";
import { Layout } from "../../components/template/Layout";

import { Dispatch } from "@reduxjs/toolkit";

import "./style.css"

import { CompactTable } from '@table-library/react-table-library/compact';
import { useTheme } from '@table-library/react-table-library/theme';
import { getTheme } from '@table-library/react-table-library/baseline';
//import { TableNode } from "@table-library/react-table-library/types";

import { useSort } from '@table-library/react-table-library/sort';
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { EventsState } from "./type";
import { RootState } from "../../";
import { getData, setData } from "../../actions/events/actions";
import { listEvents } from "../../apis";
import { useRequest } from "redux-query-react";
import { getEntities, getQueries } from "../../store";
import moment from "moment";

const EventsPage: React.FC = () => {
 //var data:any = [{url:'aaa', title:'bbb', created_at:'ccc', points:'ddd', num_components:'ff' }];

 const queries = useSelector(getQueries) || [];
 const entities = useSelector(getEntities) || [];

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

/*
 const nodes = [
  {
    id: "1",
    name: "VSCode",
    deadline: new Date(2020, 1, 17),
    type: "SETUP",
    isComplete: true
  },
  {
    id: "2",
    name: "JavaScript",
    deadline: new Date(2020, 2, 28),
    type: "LEARN",
    isComplete: true
  },
  {
    id: "3",
    name: "React",
    deadline: new Date(2020, 3, 8),
    type: "LEARN",
    isComplete: false
  }
];*/

const dispatch :Dispatch = useDispatch();

const reducer: EventsState = useSelector(
  (state: RootState) => state.eventsReducer,
  shallowEqual
)


let data:any =reducer.table;



var queryEventList = listEvents({
  queryKey: 'events_data',
   transform: (data) => {
       return {
        events_data: data,
       };
   },
   update: {
    events_data: (oldValue: any, newValue: any) => {
       return (oldValue=newValue);
     },
   }
  }
);

const [EventsListState] = useRequest(queryEventList);


if ((reducer.is_loading) && (EventsListState.isFinished)){
  console.log('aaaaa');
  dispatch(setData(entities.events_data));

}


React.useEffect(() => {
  //dispatch(getData(null));
 
});

/*
function getData(params: any) {
  return [
    {
      id: "1",
      name: "VSCode",
      deadline: new Date(2020, 1, 17),
      type: "SETUP",
      isComplete: true
    },
    {
      id: "2",
      name: "JavaScript",
      deadline: new Date(2020, 2, 28),
      type: "LEARN",
      isComplete: true
    },
    {
      id: "3",
      name: "React",
      deadline: new Date(2020, 3, 8),
      type: "LEARN",
      isComplete: false
    }
  ];
}

*/
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
  { label: 'caption', renderCell: (item:any) => item.caption,resize: true, sort: { sortKey: 'caption' } },
  { label: 'beginDate', renderCell: (item:any) => moment(item.beginDate).format('dd/MM/yyyy'),resize: true, sort: { sortKey: 'beginDate' } },
  { label: 'endDate', renderCell: (item:any) => moment(item.endDate).format('dd/MM/yyyy'),resize: true, sort: { sortKey: 'endDate' } },
  { label: 'ackDate', renderCell: (item:any) => moment(item.ackDate).format('dd/MM/yyyy'),resize: true, sort: { sortKey: 'ackDate' } },
  { label: 'position', renderCell: (item:any) => item.position,resize: true, sort: { sortKey: 'position' } },
  /*{
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
  */
 ];

  return (
    <Layout rPanel={{open:false, visible:false, 
      content:<></> 
    }} content={
    <div className={'root'}>
       <CompactTable  data={data}    theme={theme} columns={COLUMNS} sort={sort}  /> 
    </div>
    }/>
  )
}

export {EventsPage}


