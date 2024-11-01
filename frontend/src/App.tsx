import React, { useEffect } from "react";
import axios from "axios";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Planet from './pages/Planet'
import Channel from './pages/Channel'

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
        <Route path={"/"} element={<Home />} />
        <Route path={"/channel"} element={<Channel />} />
      </Routes>
    </Router>
  );
};

export default App;
