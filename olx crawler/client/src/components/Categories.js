import React from "react";
import Category from "./Category";

import "../css/Categories.css";

function Categories({ categories }) {
  return (
    <div className="Categories">
      {categories.map((category, index) => (
        <Category category={category} key={index} />
      ))}
    </div>
  );
}

export default Categories;
