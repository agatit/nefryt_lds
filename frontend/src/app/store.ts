import { configureStore, ThunkAction, Action, Dispatch } from '@reduxjs/toolkit';

import { setupListeners } from '@reduxjs/toolkit/query'
import {enhancedApi as trendApi} from '../store/trendApi'
import auth from '../features/auth/authSlice'
import template, { enqueueSnackbar } from '../features/template/templateSlice'
import charts from '../features/charts/chartsSlice'
import editor from '../features/editor/editorSlice'
import { isRejectedWithValue } from '@reduxjs/toolkit'
import type { MiddlewareAPI, Middleware } from '@reduxjs/toolkit'
import { useSnackbar } from 'notistack';
import { useDispatch } from 'react-redux';


export const rtkQueryErrorLogger: Middleware =
  (api: MiddlewareAPI) => (next) => (action) => {
    
 var state = api.getState();

 //state.template.notifications.push({message: 'Failed fetching data.' + Date.now(),
 //key: new Date().getTime() + Math.random()});

 //return;
 //state.template.enqueueSnackbar({message: 'Failed fetching data.' + Date.now(),
 //key: new Date().getTime() + Math.random()});
 
 //notifications.push({message: 'Failed fetching data.' + Date.now(),
 //key: new Date().getTime() + Math.random()});
 
 // const { enqueueSnackbar } = useSnackbar();
    console.log('FFFFFFFFFFFFFFFFFFFF');
    console.log(state);
    console.log(api);
    console.log(action);
    console.log(isRejectedWithValue(action));
    
    //api.dispatch(enqueueSnackbar({message: 'Failed fetching data.' + Date.now(),
    //key: new Date().getTime() + Math.random()}));
  
   // return state.template.enqueueSnackbar({message: 'Failed fetching data.' + Date.now(),
   // key: new Date().getTime() + Math.random()});
   
   // return;

    // RTK Query uses `createAsyncThunk` from redux-toolkit under the hood, so we're able to utilize these matchers!
    if (isRejectedWithValue(action)) {
      console.log('FFFFFFFFFFFFFFFFFFFF');
      console.warn('We got a rejected action!')
    //  addMessage('We got a rejected action!');
    //  enqueueSnackbar(action.error.data.message);
      //toast.warn({ title: 'Async error!', message: action.error.data.message })
    }

    return next(action)
  }


export const store = configureStore({
  reducer: {
    [trendApi.reducerPath] : trendApi.reducer,
    auth,
    template,
    charts,
    editor,
    
  },
  
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(rtkQueryErrorLogger),
});



export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
