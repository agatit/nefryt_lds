import { createSlice } from '@reduxjs/toolkit'
import { enhancedApi as authApi } from '../../store/authApi'
import jwt_decode from "jwt-decode";

import type { RootState } from '../../app/store'

export type AuthData={
    user: string | null | undefined; 
    token: string | null; 
    refreshToken: string | null; 
    isAuthenticated: boolean
  } 

const initialState :AuthData = {
  user: null,
  token: null,
  refreshToken:null,
  isAuthenticated: false,
}

const slice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state = initialState
    }
  },
  extraReducers: (builder) => {
    builder
      .addMatcher(authApi.endpoints.authLogin.matchPending, (state, action) => {
        console.log('pending', action)
      })
      .addMatcher(authApi.endpoints.authLogin.matchFulfilled, (state, action) => {
        //console.log('fulfilled', action);
        //console.log('LLLLLLLLLLLLLLLLLLLLLLL');
        //console.log(action.payload.token);
        state.user = action.payload.username
        state.token = action.payload.token
        state.refreshToken = action.payload.refreshToken
        localStorage.setItem('token', action.payload.token);
        localStorage.setItem('refreshToken', action.payload.token);
        localStorage.setItem('user', action.payload.token);
        state.isAuthenticated = true
      })
      .addMatcher(authApi.endpoints.authLogin.matchRejected, (state, action) => {
        console.log('rejected', action)
      })
      .addMatcher(authApi.endpoints.authRefresh.matchFulfilled, (state, action) => {
        console.log(action.payload);
        state.user = action.payload.username
        state.token = action.payload.token
        state.refreshToken = action.payload.refreshToken
        state.isAuthenticated = true
      })
      .addMatcher(authApi.endpoints.authRefresh.matchRejected, (state, action) => {
        state = initialState;
      });
  },
})

export const { logout } = slice.actions
export default slice.reducer

export const selectIsAuthenticated = (state: RootState) =>{
    var token = localStorage.getItem('token');
    if (token){
      const decodedToken: { exp: number } = jwt_decode(token);
        let currentDate = new Date();
        console.log(decodedToken.exp * 1000);
        console.log(currentDate.getTime());
        console.log(currentDate.getTime() - decodedToken.exp * 1000);
        if (decodedToken.exp * 1000 < currentDate.getTime()) {
          console.log('refresh');
          }else{
            return true;
          }
    }
  
    return false
}