import './styles.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import {EditorPage} from './pages/Editor'
import { DashboardPage } from "./pages/Dashboard";
import { ChartsPage } from "./pages/Charts";
import { EventsPage } from "./pages/Events";
import { NoPageFound } from "./pages/Error/404";
import { useListTrendsQuery } from './store/trendApi';

import { AuthLoginApiArg, AuthLoginApiResponse, Login, useAuthLoginMutation, useAuthRefreshMutation } from './store/authApi';
import { UseMutationStateOptions } from '@reduxjs/toolkit/dist/query/react/buildHooks';
import { useEffect } from 'react';
import LoginPage from './pages/User/Login';
import {
  Link,
  Navigate,
  Outlet,
} from 'react-router-dom';
import { AuthData, selectIsAuthenticated } from './features/auth/authSlice';
import {  shallowEqual, useSelector } from 'react-redux';
import { RootState, store } from './app/store';
import jwt_decode from "jwt-decode";

const ProtectedRoute = ({ user=false, redirectPath = '/login' }) => {
  if (!user) {
    return <Navigate to={redirectPath} replace />;
  }

  return <Outlet />;
};

export default function App() {
  
  const isAuthenticated = useSelector(selectIsAuthenticated)
  //const isAuthenticated = true;


  const auth: AuthData = useSelector(
    (state: RootState) => state.auth,
    shallowEqual
  )

  


const [
  refreshTokenPost,          // This is the mutation trigger
  { isLoading: isUpdating }, // This is the destructured mutation result

] = useAuthRefreshMutation();


  return (
    <div className="App">
       <Router>
          <Routes>
              <Route element={<ProtectedRoute user={isAuthenticated} />}>
                  <Route path='/' element={<DashboardPage/>} />
                
              <Route path='/editor' element={<EditorPage/>} />
              <Route path='/events' element={<EventsPage/>} />
              <Route path='/charts' element={<ChartsPage/>} />
              </Route> 
              <Route path='/login' element={<LoginPage/>} />
              <Route path="*" element={<NoPageFound/>}/>
              
          </Routes>
      </Router>
    </div>
  );
}


