import * as React from "react"
import { render } from "react-dom"
import ReactDOM from 'react-dom/client';
import { applyMiddleware, Store } from "redux"
import { Provider } from "react-redux"
import thunk from "redux-thunk"
import App from "./App"

import { configureStore } from "@reduxjs/toolkit";
import { createBrowserHistory } from 'history';
import { routerMiddleware, connectRouter } from 'connected-react-router';
// import { Provider as ReduxQueryProvider } from "redux-query-react";
// import superagentInterface from 'redux-query-interface-superagent';
// import { queryMiddleware } from "redux-query";
// import { QueryClient, QueryClientProvider } from "react-query";
// import {  createStore, combineReducers } from 'redux';
// import reducer, { getEntities,  getQueries } from './store/index'



export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
var container = document.querySelector("#root");
const root =ReactDOM.createRoot(container==null?new Element() : container);

const queryClient = new QueryClient();


root.render( <Provider store={store}>
  {/*<QueryClientProvider client={queryClient}>*/}
  <ReduxQueryProvider queriesSelector={getQueries}>
  <App />
  </ReduxQueryProvider>
  {/*</QueryClientProvider>*/}
  </Provider>
)


