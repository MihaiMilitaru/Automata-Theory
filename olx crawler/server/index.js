const express = require("express");
const { spawn } = require("child_process");
const cors = require("cors");
const app = express();
const port = 3001;

// The cors library is used to prevent CORS to allow backend calls from a different origin
app.use(cors());

// The route that is called from the React frontend.
// It will spawn a python process that runs the crawler script
// Once it ends, it calls the regex script and passes the object containing
// all the information to the client
app.get("/categories", (req, res) => {
  const crawlerPython = spawn("python", ["crawler.py"]);
  crawlerPython.on("close", (code) => {
    console.log("Stopping crawler...");
    let data = [];
    const regexPython = spawn("python", ["regex.py"]);
    // Data printed by the python file is taken by the script using the stdout.on method
    regexPython.stdout.on("data", (d) => {
      console.log("Running regex...");
      data.push(d);
    });

    // Set the data sent as JSON
    regexPython.on("close", (code) => {
      console.log("Stopping regex...");
      res.setHeader("Content-Type", "application/json");
      res.send(data.join(""));
    });
  });
});

app.listen(port, () => console.log(`Listening on port ${port}`));
