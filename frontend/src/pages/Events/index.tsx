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
import { getData } from "../../actions/events/actions";

const EventsPage: React.FC = () => {
 //var data:any = [{url:'aaa', title:'bbb', created_at:'ccc', points:'ddd', num_components:'ff' }];


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

//dispatch(getData(null)); 

let data:any =reducer.table.data;
console.log(data);



/*const doGet = React.useCallback(async (params:any) => {
  data= {nodes}; //getData(params);
  console.log(data);
}, []);

doGet({});
*/
React.useEffect(() => {
  //doGet({});
 
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
console.log('fffff');
  getData(params);
  console.log('lllll');
   // getData(params); 
}

//console.log('BBBBBB');
//setTimeout(function() {
  //getGridData(null);
//  console.log('AAAAA');
//}, 3000);

 /*
 const sort = useSort(
  data,
  {
    onChange: onSortChange,
  },
  {
    sortFns: {
      TASK: (array) => array.sort((a, b) => a.name.localeCompare(b.name)),
      DEADLINE: (array) => array.sort((a, b) => a.deadline - b.deadline),
      TYPE: (array) => array.sort((a, b) => a.type.localeCompare(b.type)),
      COMPLETE: (array) => array.sort((a, b) => a.isComplete - b.isComplete),
      TASKS: (array) => array.sort((a, b) => (a.nodes || []).length - (b.nodes || []).length),
    },
  },
);

function onSortChange(action:any, state:any) {
  console.log(action, state);
}
*/ 
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


