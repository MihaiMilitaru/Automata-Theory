import React from "react";
import { useState } from "react";

import "../css/Category.css";

function Category({ category }) {
  const listItems = Object.entries(category.counters);
  const [showAll, setShowAll] = useState(false);

  return (
    <div className="Category">
      <h1 className="Category__title">{category.name}</h1>
      <ul className="Category__list">
        {listItems.map(([countItem, count]) =>
          showAll ? (
            <li className="Category__list__item" key={countItem}>
              {countItem} ----{">"}{" "}
              <span className="Category__last__item__count">{count}</span>
            </li>
          ) : count ? (
            <li className="Category__list__item" key={countItem}>
              {countItem} ----{">"}{" "}
              <span className="Category__last__item__count">{count}</span>
            </li>
          ) : null
        )}
        {!listItems.every(([countItem, count]) => count) && (
          <button
            className="Category__list__show"
            onClick={() => setShowAll(!showAll)}
          >
            {showAll ? "Active" : "All"}
          </button>
        )}
      </ul>
    </div>
  );
}

export default Category;
