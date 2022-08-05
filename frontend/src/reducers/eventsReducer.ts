import { getData } from "../actions/events/actions";
import { GET_DATA, SET_DATA } from "../actions/events/actionType";
import { EventsState, IEventsAction } from "../pages/Events/type";
//import { getDefaultMiddleware } from '@reduxjs/toolkit';

//const customizedMiddleware = getDefaultMiddleware({
//  serializableCheck: false
//})

function getGridData(params:any): any {
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
  ];

  return {nodes};
}


const initialState: EventsState = {
    table: {nodes  :   [],
      pageInfo: null
    },
    is_loading : true
  }



const eventsReducer = (
    state: EventsState = initialState,
    action: IEventsAction
  ): EventsState => {

    switch (action.type) {
        case SET_DATA:{
          //var data = getGridData(action.data);
          console.log(action.data);
          return {
            ...state,
            table: {nodes: action.data, pageInfo:state.table.pageInfo}, is_loading:false
          }
        }
        case GET_DATA:{
          return {
            ...state,
            table: state.table, is_loading:true
          }
        }
        

       
    }
    return state
  }
  
  export default eventsReducer


