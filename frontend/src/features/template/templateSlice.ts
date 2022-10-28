import { display } from '@mui/system'
import { createSlice } from '@reduxjs/toolkit'
import actions from 'redux-form/lib/actions'


export type templateState = {
  sidebar_open:boolean,
  notifications: any[],
  displayed: any[]
}

var init  : templateState = {
  sidebar_open: false,
  notifications: [],
  displayed: []
}

export const templateSlice = createSlice({
  name: 'template',
  initialState: init,
  reducers: {
    toggleSidebar: (state) => {
      // Redux Toolkit allows us to write "mutating" logic in reducers. It
      // doesn't actually mutate the state because it uses the immer library,
      // which detects changes to a "draft state" and produces a brand new
      // immutable state based off those changes
      state.sidebar_open = !state.sidebar_open;
    },
    enqueueSnackbar: (state, action) => {
      //const key = notification.payload.options && notification.payload.options.key;
      for (var x=0; x<state.displayed.length; x++){
        state.notifications = state.notifications.filter((notification: any) => notification.key!=state.displayed[x]);
      }
       state.notifications.push(action.payload);
    },
    setDisplayedSnackbar : (state,action) =>{
      state.displayed.push(action.payload);
    }
  },
  extraReducers: (builder) => {
    builder
    .addMatcher((action) =>  action.type.endsWith('/rejected'),// && action.payload.status === "FETCH_ERROR",
    (state, action) => {
      if ((action.payload) && (action.payload.status) && (action.payload.status === "FETCH_ERROR")){ 
      for (var x=0; x<state.displayed.length; x++){
        state.notifications = state.notifications.filter((notification: any) => notification.key!=state.displayed[x]);
      }
      state.notifications.push({message: 'Błąd połaczenia z serwerem.', options:{variant:'error'},
      key: new Date().getTime() + Math.random()});
    }
    })
    .addMatcher((action) =>  action.type.endsWith('/rejected'),  (state, action) => {
       if ((action.payload) && (action.payload.data) && (action.payload.data.code >=400) && (action.payload.data.code <500)){  
        for (var x=0; x<state.displayed.length; x++){
          state.notifications = state.notifications.filter((notification: any) => notification.key!=state.displayed[x]);
        }
        state.notifications.push({message: 'Brak uprawnień do wykonania zadania!.', options:{variant:'warning'},
        key: new Date().getTime() + Math.random()});
       }
    })
    .addMatcher((action) =>  action.type.endsWith('/rejected'),  (state, action) => {
      if ((action.payload) && (action.payload.data)&&(action.payload.data.code >=500) && (action.payload.data.code <600)){  
       for (var x=0; x<state.displayed.length; x++){
         state.notifications = state.notifications.filter((notification: any) => notification.key!=state.displayed[x]);
       }
       state.notifications.push({message: 'Błąd połaczenia z serwerem!.', options:{variant:'warning'},
       key: new Date().getTime() + Math.random()});
      }
   })
  }
})

export const { toggleSidebar, enqueueSnackbar, setDisplayedSnackbar} = templateSlice.actions

// The function below is called a thunk and allows us to perform async logic. It
// can be dispatched like a regular action: `dispatch(incrementAsync(10))`. This
// will call the thunk with the `dispatch` function as the first argument. Async
// code can then be executed and other actions can be dispatched


// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state) => state.counter.value)`

//export const selectTemplate = (state) => state.template.value

export default templateSlice.reducer
