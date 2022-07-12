import { combineReducers } from 'redux'
import templateReducer from '../reducers/templateReducer'
import chartsReducer from '../reducers/chartsReducer'
import eventsReducer from '../reducers/eventsReducer'
import pipelineEditorReducer from '../reducers/pipelineEditorReducer'
import propertyEditorReducer from '../reducers/propertyEditorReducer'

import { entitiesReducer, EntitiesSelector, queriesReducer, QueriesState } from "redux-query";
import { Trend, TrendData } from '../models';

export type EntitiesState = {
  trends_data: TrendData[],
  trends_live_data: TrendData[],
  trends_list:Trend[]
}

export const getQueries = (state: { queries: QueriesState; }) => state.queries;
export const getEntities = (state: { queries: QueriesState; entities: EntitiesState; }) => state.entities;



const reducer = combineReducers({
    templateReducer,
    chartsReducer,
    eventsReducer,
    entities: entitiesReducer,
    queries: queriesReducer,
    pipelineEditorReducer,
    propertyEditorReducer,
    //form:forms,
    //
    //dashboardReducer,
    
});

export default reducer