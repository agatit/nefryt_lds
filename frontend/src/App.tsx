import React from 'react';
import logo from './logo.svg';
import './App.css';

import {EditorPage} from './pages/Editor'
import { DashboardPage } from "./pages/Dashboard";
import { ChartsPage } from "./pages/Charts";
import { EventsPage } from "./pages/Events";
import { NoPageFound } from "./pages/Error/404";

import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";


function App() {
  return (
    <div className="App">
       <Router>
          <Routes>
              <Route path='/' element={<DashboardPage/>} />
              <Route path='/editor' element={<EditorPage/>} />
              <Route path='/events' element={<EventsPage/>} />
              <Route path='/charts' element={<ChartsPage/>} />
              <Route path="*" element={<NoPageFound/>}/>
          </Routes>
      </Router>
    </div>
  );
}

export default App;
