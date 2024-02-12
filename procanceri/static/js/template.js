function showdata() {
  const userData = JSON.parse(sessionStorage.getItem("selected"));
  console.log(Object.keys(userData));
  const generalData=JSON.parse(sessionStorage.getItem("generalinfo"));
  create_title(generalData.task_name);
  createtable(userData);


}

function create_title(title){
  const newDiv = document.createElement("div");
  const newContent = document.createTextNode(title);
  newDiv.style.fontSize = "20px";  newDiv.appendChild(newContent);
  const currentDiv = document.getElementById("table-container");
  newDiv.style.background = "linear-gradient(rgb(0, 31, 84), rgb(27, 153, 244))";
  newDiv.style.width= "250px";
  newDiv.style.height="250px";
  newDiv.style.color= "white";
  newDiv.style.margin="0px;"
  newDiv.style.paddingTop = "20%";
  newDiv.style.borderRadius = "5%";
  newDiv.style.textAlign="center";
  
  document.getElementById("title").appendChild(newDiv);

}







function createtable(jsondata) {
  const table = document.createElement("table");
  const tableContainer = document.getElementById("table-container");
  for (key in jsondata) {
    if (jsondata.hasOwnProperty(key)) {
      if (key === "AI_Developer") {
        const arr = key.split("_");
        var k = arr.join(" ");
        tableContainer.innerHTML +=
        "<h2 class='display-7'style='font-weight: bold; text-align: center; width:100%;'  >" +
        k +
        "</h2>";
      }else{

      tableContainer.innerHTML +=
        "<h2 class='display-7'style='font-weight: bold; text-align: center; width:100%;'  >" +
        key+
        "</h2>";
      }

      create_table(jsondata[key], tableContainer, key);
    }
  }
}
function showSelectedOption() {
  var selectElement = document.getElementById("options");

  var selectedOption = selectElement.value;

  var infoElement = document.getElementById(selectedOption);

}
function create_table(jsonData, tableContainer, key) {
  const table = document.createElement("table");

  for (const key in jsonData) {
    if (jsonData.hasOwnProperty(key)) {
      const value = jsonData[key];

      const row = table.insertRow();

      const keyCell = row.insertCell(0);
      keyCell.textContent = key;

      const valueCell = row.insertCell(1);
      valueCell.textContent = value;
    }
  }

  tableContainer.appendChild(table);
}

