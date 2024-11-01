import React, { useEffect, useState } from "react";
import axios from "axios";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Planet from './pages/Planet'
import Gateway from './pages/Gateway'
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
  const [userId, setUserId] = useState<number>(0);
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <Router>
      <Routes>
        <Route path={"/"} element={<Home userId={userId} setUserId={setUserId}/>} />
        <Route path={"/gateway"} element={<Gateway userId={userId} setUserId={setUserId}/>} />
        <Route path={"/channel"} element={<Channel userId={userId} setUserId={setUserId}/>} />
        <Route path="/planet/:planetUserId" element={<Planet userId={userId} setUserId={setUserId}/>} />
      </Routes>
    </Router>
  );
};

export default App;
