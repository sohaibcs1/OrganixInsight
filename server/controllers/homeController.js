// import { client } from '../socket/index.js';
import { client } from '../socket/index.js';

// const getUserNames = async ({ token, name }) => {
//   return await new Promise(resolve => {
//     client.on("reponse", function(data) {
//       resolve(data);
//     })
//     client.emit("respond");
//   })
// }
// npm install socket.io
// console.log(client)
const getNumbers = async () => {
  console.log("get numbers called");
  return await new Promise(resolve => {
    client.on("numbers", (data) => {
      console.log({
        data
      })
      resolve(data);
    })
    client.emit("getNumbers");
  })
}

const getHeatmap = async (name) => {
  console.log("Heatmap function call called");
  return await new Promise(resolve => {
    client.on("heatmap", (data) => {
      console.log({
        data
      })
      resolve(data);
    })
    client.emit("getHeatmap",name);
  })
}

const getHeatmap_basal = async (name) => {
  console.log("Heatmap function call called");
  return await new Promise(resolve => {
    client.on("heatmap_basal", (data) => {
      console.log({
        data
      })
      resolve(data);
    })
    client.emit("getHeatmap_basal",name);
  })
}

const getbasal = async (name) => {
  console.log("basal/non function call called");
  return await new Promise(resolve => {
    client.on("basal", (data) => {
      console.log({
        data
      })
      resolve(data);
    })
    client.emit("getbasal",name);
  })
}

// const getpositive = async (name) => {
//   console.log("Positive cells function call called");
//   return await new Promise(resolve => {
//     client.on("positive", (data) => {
//       console.log({
//         data
//       })
//       resolve(data);
//     })
//     client.emit("getpositive",name);
//   })
// }


const getpositive = async (payload) => {
  console.log("Positive cells function call called");
  return await new Promise(resolve => {
    client.on("positive", (data) => {
      console.log({
        data
      })
      resolve(data);
    })
    client.emit("getpositive",payload);
  })
}

const getpositive_input = async (name) => {
  console.log("Positive cells function call called");
  return await new Promise(resolve => {
    client.on("positive_input", (data) => {
      console.log({
        data
      })
      resolve(data);
    })
    client.emit("getpositive_input",name);
  })
}

const getPositiveBarplot = async (name) => {
  console.log("Positive barplot function called");
  return await new Promise(resolve => {
    client.on("positive_barplot", (data) => {
      console.log({
        data
      })
      resolve(data);
    })
    client.emit("getPositiveBarplot",name);
  })
}

const getCellcount = async (name) => {
  console.log("getCellcount function call called");
  return await new Promise(resolve => {
    client.on("cellcount", (data) => {
      console.log({
        data
      })
      resolve(data);
    })
    client.emit("getCellcount",name);
  })
}

const getCc = async (name) => {
  console.log("getCc function call called");
  return await new Promise(resolve => {
    client.on("cccluster", (data) => {
      console.log({
        data
      })
      resolve(data);
    })
    client.emit("getCc",name);
  })
}

const getParaviewUrl = async (name) => {
  console.log("get Paraview URL called");
  return await new Promise(resolve => {
    client.on("url", (data) => {
      console.log({
        data
      })
      resolve(data);
    })
    client.emit("getParaviewUrl", name ); // Pass the variable to the server
  })
}

const getAnalysis = async (name) => {
  console.log("get analyss called");
  return await new Promise(resolve => {
    client.on("numbers", (data) => {
      console.log({
        data
      })
      resolve(data);
    })
    client.emit("getAnalysis", name ); // Pass the variable to the server
  })
}



const processFiles = async () => {
  console.log("process file function call");
  return await new Promise(resolve => {
    client.on("response", (data) => {
      console.log({
        data
      })
      resolve(data);
    })
    client.emit("processFiles");
  })
}

const processFilesbulk = async (info) => {
  console.log("process file function call");
  return await new Promise(resolve => {
    client.on("response", (data) => {
      console.log({
        data
      })
      resolve(data);
    })
    client.emit("processFilesbulk",info);
  })
}

export default {
  // getUserNames,
  getNumbers,processFiles,processFilesbulk,getParaviewUrl,getAnalysis,getHeatmap,getHeatmap_basal,getbasal,getpositive,getpositive_input,getCellcount,getCc,getPositiveBarplot
}
