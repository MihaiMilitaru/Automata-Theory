import React from "react";

import "../css/Loading.css";
import loader from "../imgs/loading.gif";

function Loading() {
  return (
    <div className="Loading">
      <img src={loader} alt="loader" />
    </div>
  );
}

export default Loading;
