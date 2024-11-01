import React, { useEffect } from "react";
import axios from "axios";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'

const fetchData = async () => {
  try {
    const response = await axios.get("http://localhost:8000/hi");
    console.log(response.data);
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

const App: React.FC = () => {
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <Router>
      <Routes>
        <Route path={"/"} element={<Planet />} />
      </Routes>
    </Router>
  );
};

export default App;
