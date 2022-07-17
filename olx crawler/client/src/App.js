import React from "react";
import { useState } from "react";
import axios from "axios";

import Categories from "./components/Categories";
import Loading from "./components/Loading";
import { useTitle } from "./components/useTitle";

import "./css/App.css";
import "./css/global.css";

function App() {
  const [data, setData] = useState();
  const [showLoading, setShowLoading] = useState(false);

  const handleOnClick = () => {
    setShowLoading(true);
    axios
      .get("http://localhost:3001/categories")
      .then((response) => setData(response.data));
  };

  // data && console.log(data);
  useTitle("Olx Crawler");
  return (
    <div className="App">
      {!showLoading && (
        <button className="App__button" onClick={handleOnClick}>
          Start crawler
        </button>
      )}
      {data ? (
        <Categories categories={data} />
      ) : showLoading ? (
        <Loading />
      ) : null}
    </div>
  );
}

export default App;
