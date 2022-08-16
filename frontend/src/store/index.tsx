import { combineReducers } from 'redux'
import templateReducer from '../reducers/templateReducer'
import chartsReducer from '../reducers/chartsReducer'
import eventsReducer from '../reducers/eventsReducer'
import pipelineEditorReducer from '../reducers/pipelineEditorReducer'
import propertyEditorReducer from '../reducers/propertyEditorReducer'

import { configureStore } from '@reduxjs/toolkit'
import { Pipeline } from './pipelineApi';
import { Trend, TrendData } from './trendApi';
import { api } from './emptyApi';

import { reducer as forms  } from 'redux-form';

export type EntitiesState = {
  trends_data: TrendData[],
  trends_live_data: TrendData[],
  trends_list:Trend[],
  pipeline_list:Pipeline[],
  node_list : Array<Node>,
  events_data: Array<Event>
}

// export const getQueries = (state: { queries: QueriesState; }) => state.queries;
// export const getEntities = (state: { queries: QueriesState; entities: EntitiesState; }) => state.entities;



const reducer = combineReducers({
    templateReducer,
    chartsReducer,
    eventsReducer,
    pipelineEditorReducer,
    propertyEditorReducer,
    form:forms,
    api.reducer,
});


export const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
  },
  // adding the api middleware enables caching, invalidation, polling and other features of `rtk-query`
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
})


export const history = createBrowserHistory();
/*
const store = createStore(  
  reducer,
  applyMiddleware(queryMiddleware(superagentInterface, getQueries, getEntities)),
);
*/

const store = configureStore({reducer, 
  middleware: [thunk, routerMiddleware(history), queryMiddleware(superagentInterface, getQueries, getEntities)],
})

export default reducer