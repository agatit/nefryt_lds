import { configureStore, ThunkAction, Action } from '@reduxjs/toolkit';

import { setupListeners } from '@reduxjs/toolkit/query'
import {enhancedApi as trendApi} from '../store/trendApi'
import auth from '../features/auth/authSlice'
import template from '../features/template/templateSlice'
import charts from '../features/charts/chartsSlice'
import editor from '../features/editor/editorSlice'

export const store = configureStore({
  reducer: {

    [trendApi.reducerPath] : trendApi.reducer,
    //[trendApi.reducerPath] : trendApi.reducer,
    auth,
    template,
    charts,
    editor
    
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(trendApi.middleware),
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
