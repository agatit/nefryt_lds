import { combineReducers } from 'redux'
import templateReducer from '../reducers/templateReducer'
import chartsReducer from '../reducers/chartsReducer'
import eventsReducer from '../reducers/eventsReducer'

import { entitiesReducer, EntitiesSelector, queriesReducer, QueriesState } from "redux-query";
import { Trend, TrendData } from '../models';

export type EntitiesState = {
  trends_data: TrendData[],
  trends_list:Trend[]
}

export const getQueries = (state: { queries: QueriesState; }) => state.queries;
export const getEntities = (state: { queries: QueriesState; entities: EntitiesState; }) => state.entities;

/*
export const notificationsRequest = {
  queryKey: 'notificationData',
  url: 'http://192.168.1.231:8080/trend/101,102/data/1627983649/1627983659/100',
  transform: (responseBody: { data: any; }) => {
    console.log(responseBody);
    return {
      notifications: responseBody,
    };
  },
  update: {
    notifications: (oldValue: any, newValue: any) => {
      console.log(oldValue);
      console.log(newValue);
      return (oldValue = newValue);
    },
  }, 
};
*/

const reducer = combineReducers({
    templateReducer,
    chartsReducer,
    eventsReducer,
    entities: entitiesReducer,
    queries: queriesReducer

    //pipelineEditorReducer,
    //propertyEditorReducer,
    //form:forms,
    //
    //dashboardReducer,
    
});

export default reducer