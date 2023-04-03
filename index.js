const express = require("express");
const app = express();
const path = require("path");

const axios = require("axios");

const csv = require("csv-parser");
const fs = require("fs");

//For running python scripts
const { spawn } = require("child_process");

const port = process.env.PORT || 3000;

app.use(express.json());


function deleteFilesOnStartup(directoryPath, filesToDelete) {
  fs.readdir(directoryPath, (err, files) => {
    if (err) {
      console.error('Error reading the directory:', err);
      return;
    }

    files.forEach((file) => {
      if (filesToDelete.includes(file)) {
        const filePath = path.join(directoryPath, file);
        fs.unlink(filePath, (err) => {
          if (err) {
            console.error('Error deleting the file:', err);
            return;
          }
          console.log('Deleted:', filePath);
        });
      }
    });
  });
}

const filesDirectory = './data';
const filesToDelete = ['cowrie.csv', 'cowrie.json'];
deleteFilesOnStartup(filesDirectory, filesToDelete);

// Serve static files from the static directory
app.use(express.static(path.join(__dirname, "static")));

// Displays the index.html file in the home page.
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "static/index.html"));
});

function runPythonScript(scriptPath, inputFileName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn("python", [scriptPath, inputFileName]);

    pythonProcess.stderr.on("data", (data) => {
      console.error(`Python error: ${data}`);
      reject(data);
    });

    pythonProcess.on("close", (code) => {
      console.log(`Python process exited with code ${code}`);
      resolve(code);
    });
  });
}

// Running conversion script
app.post("/convert", async (req, res) => {
  const script = "./scripts/conversion-script.py";
  const inputFile = "./data/cowrie.json.11.gz";

  if (!script || !inputFile) {
    return res
      .status(400)
      .json({ error: "Both script and inputFile must be provided." });
  }

  try {
    await runPythonScript(script, inputFile);
    res.status(200).json({ message: "Script executed successfully." });
  } catch (error) {
    res.status(500).json({ error: "Error executing the script." });
  }
});

// Running multiple scripts to preprocess data
app.post("/preprocess", async (req, res) => {
  // Set hardcoded script and inputFile values
  const scriptsAndInputFiles = [
    {
      script: "./scripts/command-extract-new.py",
      inputFile: "./data/cowrie.csv",
    },
    {
      script: "./scripts/destfile-and-login-new.py",
      inputFile: "./data/cowrie.csv",
    },
    {
      script: "./scripts/filter-and-timestamp-new.py",
      inputFile: "./data/cowrie.csv",
    },
    { script: "./scripts/prepare-new.py", inputFile: "./data/cowrie.csv" },
    // Add more scripts and input files as needed
  ];

  try {
    for (const { script, inputFile } of scriptsAndInputFiles) {
      await runPythonScript(script, inputFile);
    }
    res.status(200).json({ message: "All scripts executed successfully." });
  } catch (error) {
    res.status(500).json({ error: "Error executing the scripts." });
  }
});

app.post("/classify_tactics", (req, res) => {
  const pythonProcess = spawn("python", ["./algorithm/classify.py"]);

  pythonProcess.stdout.on("data", (data) => {
    console.log(`stdout: ${data}`);
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    console.log(`child process exited with code ${code}`);
    if (code === 0) {
      res.status(200).json({ message: "All scripts executed successfully." });
    } else {
      res.status(500).json({ error: "Error executing the scripts." });
    }
  });
});

const csvFilePath = "data/cowrie.csv";

// Define an endpoint that returns JSON data from the CSV file
app.get("/data", (req, res) => {
  const results = [];
  let count = 0;
  fs.createReadStream(csvFilePath)
    .pipe(csv())
    .on("data", (data) => {
      if (count < 25) {
        results.push(data);
        count++;
      }
    })
    .on("end", () => {
      res.json(results);
    });
});

// Define your API key
const apiKey =
  "306b0c30d9020d5734b09bd463705f980a7724d0d02dd6d09be9806ba4f1e7157d5db545ff5408ba";

// Define a route with a parameter for the IP address
app.get("/ipinfo/:ip", (req, res) => {
  // Get the IP address from the parameter
  const ipAddress = req.params.ip;

  // Make a GET request to the AbuseIPDB CHECK endpoint
  axios
    .get("https://api.abuseipdb.com/api/v2/check", {
      params: {
        ipAddress: ipAddress,
        maxAgeInDays: 90,
        verbose: true,
      },
      headers: {
        Key: apiKey,
        Accept: "application/json",
      },
    })
    .then((response) => {
      // Handle success
      // console.log(response.data);

      // Destructure the data object from the response object
      const { data } = response.data;

      // Destructure the data object to get only the abuseConfidenceScore, countryName and isp
      const { abuseConfidenceScore, countryName, isp } = data;

      // Create a new object with only those properties
      const ipInfo = { abuseConfidenceScore, countryName, isp };

      // console.log(ipInfo);
      // Send the ipInfo object to the front end
      res.json(ipInfo);
    })
    .catch((error) => {
      // Handle error
      console.error(error);

      // Send an error message to the front end
      res.status(500).send("Something went wrong");
    });
});

app.listen(port, () => console.log(`SERVER STARTED ON PORT: ${port} 🫡`));
