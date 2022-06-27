import { getData } from "../actions/events/actions";
import { GET_DATA } from "../actions/events/actionType";
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

 
  //console.log({nodes});

  //dispatch(nodes);
  return {nodes};
}





const initialState: EventsState = {
    table: {data  :   getGridData(null),
      pageInfo: null
    }
  }

//  const initialState: EventsState = {
//    table: {data  :  getGridData({})}
//  }

const eventsReducer = (
    state: EventsState = initialState,
    action: IEventsAction
  ): EventsState => {

    switch (action.type) {
        case GET_DATA:{
          var data = getGridData(action.data);
          console.log(data);
          return {
            ...state,
            table: {data: data, pageInfo:state.table.pageInfo}
          }
        }
        

       
    }
    return state
  }
  
  export default eventsReducer


