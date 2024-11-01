import React, { useEffect } from "react";
import axios from "axios";

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
    <div>
      <h1>Hello from React!!!!</h1>
    </div>
  );
};

export default App;
