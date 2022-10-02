import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './WebScrapper';
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/users' element={<App/>}/>
        <Route path='/users/:userName/repositories' element={<App/>}/>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);



