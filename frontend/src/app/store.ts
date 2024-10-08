import { configureStore, ThunkAction, Action, Dispatch } from '@reduxjs/toolkit';

import { setupListeners } from '@reduxjs/toolkit/query'
import {enhancedApi as trendApi} from '../store/trendApi'
import auth from '../features/auth/authSlice'
import {enhancedApi as authApi} from '../store/authApi'
import template, { enqueueSnackbar } from '../features/template/templateSlice'
import charts from '../features/charts/chartsSlice'
import editor from '../features/editor/editorSlice'
import nodeEditor from '../features/editor/nodeEditorSlice'
import { isRejectedWithValue } from '@reduxjs/toolkit'
import type { MiddlewareAPI, Middleware } from '@reduxjs/toolkit'
import { useSnackbar } from 'notistack';
import { useDispatch } from 'react-redux';
import { api } from '../store/emptyApi';
import trendEditor from '../features/editor/trendEditorSlice'



export const store = configureStore({
  reducer: {
    [trendApi.reducerPath] : trendApi.reducer,
    auth,
    template,
    charts,
    editor,
    nodeEditor,
    trendEditor
  },
  
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
});



export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
