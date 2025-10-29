import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import Home from '@pages/Home/Home'
import Models from '@pages/Models/Models'
import ModelDetails from '@pages/Models/ModelDetails'
import ModelCreation from '@pages/ModelCreation/ModelCreation'
import { ChatbotWidget } from "laredocmind";

import './App.css'

function App() {
  return(
    <><ChatbotWidget apiUrl="/chatbot" />
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/models' element={<Models />} />
        <Route path='/models/:modelName' element={<ModelDetails />} />
        <Route path='/model-creation' element={<ModelCreation />} />
      </Routes>
    </>
  );
}

export default App
