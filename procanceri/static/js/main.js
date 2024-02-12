var selected = {};
var other = {};
function showSelectedOption() {
  var selectElement = document.getElementById("options");

  var selectedOption = selectElement.value;
  // alert(selectedOption);

  hideAllInformation();

  var infoElement = document.getElementById("infoOption_" + selectedOption);
  // alert(infoElement);

  if (infoElement) {
    infoElement.style.display = "block";
    hideAllmoreInformation();
  }
}

function hideAllInformation() {
  var infoElements = document.getElementsByClassName("info");
  for (var i = 0; i < infoElements.length; i++) {
    infoElements[i].style.display = "none";
  }
}
function hideAllmoreInformation() {
  var infoElements = document.getElementsByClassName("someinfostable");
  var mybutton = document.getElementById("showinfo");
  mybutton.innerHTML = "Show more info";
  for (var i = 0; i < infoElements.length; i++) {
    infoElements[i].hidden = true;
    document.getElementById("h2dummy").hidden = true;
    document.getElementById("h1dummy").hidden = true;
    document.getElementById("h3dummy").hidden = true;
  }
  var otheroptions = {};
  var other = document.getElementById("someinfos");
  //alert(other);

  var ss = other.getElementsByTagName("input");
  for (i = 0; i < ss.length; i++) {
    if (ss[i].type != "checkbox") continue;
    ss[i].checked = false;
  }
}

function showmoreinfo() {
  var mybutton = document.getElementById("showinfo");
  var selectElement = document.getElementById("options");

  var selectedOption = selectElement.value;
  switch (selectedOption) {
    case "AI_Developer":
      var infoElement1 = document.getElementById("Patient_more_info");
      var infoElement2 = document.getElementById("Clinical_more_info");
      if (infoElement1.hidden === true && infoElement1.hidden === true) {
        infoElement1.hidden = false;
        infoElement2.hidden = false;
        document.getElementById("h2dummy").hidden = false;
        document.getElementById("h3dummy").hidden = false;

        mybutton.innerHTML = "Hide info";
      } else {
        infoElement1.hidden = true;
        infoElement2.hidden = true;
        mybutton.innerHTML = "Show More Info";
        document.getElementById("h2dummy").hidden = true;
        document.getElementById("h3dummy").hidden = true;
      }

      break;
    case "Clinical":
      var infoElement1 = document.getElementById("AI_Developer_more_info");
      var infoElement2 = document.getElementById("Patient_more_info");
      if (infoElement1.hidden === true && infoElement1.hidden === true) {
        infoElement1.hidden = false;
        infoElement2.hidden = false;
        document.getElementById("h1dummy").hidden = false;
        document.getElementById("h3dummy").hidden = false;

        mybutton.innerHTML = "Hide info";
      } else {
        infoElement1.hidden = true;
        infoElement2.hidden = true;
        mybutton.innerHTML = "Show More Info";
        document.getElementById("h3dummy").hidden = true;
        document.getElementById("h1dummy").hidden = true;
      }
      break;
    case "Patient":
      var infoElement1 = document.getElementById("AI_Developer_more_info");
      var infoElement2 = document.getElementById("Clinical_more_info");
      if (infoElement1.hidden === true && infoElement1.hidden === true) {
        infoElement1.hidden = false;
        infoElement2.hidden = false;
        document.getElementById("h1dummy").hidden = false;
        document.getElementById("h2dummy").hidden = false;

        mybutton.innerHTML = "Hide info";
      } else {
        infoElement1.hidden = true;
        infoElement2.hidden = true;
        mybutton.innerHTML = "Show More Info";
        document.getElementById("h1dummy").hidden = true;
        document.getElementById("h2dummy").hidden = true;
      }

      break;
    case "Dummy4":
      // alert("dumm4");
      break;
  }

  document.getElementById("someinfos").style.display = "block";
}

function generateinfo() {
  selected = {};
  var selectElement = document.getElementById("options");

  var selectedOption = selectElement.value + "_info";
  if (hasvalue()) {
    var checkbox_all = document.getElementById(selectedOption);
    var inputElements = checkbox_all.getElementsByTagName("input");
    for (i = 0; i < inputElements.length; i++) {
      if (inputElements[i].type != "checkbox") continue;
      if (inputElements[i].checked === true) {
        selected[inputElements[i].name] = inputElements[i].value;
      }
    }
    var titles = selectElement.value;
    var nestedJSON = {};
    nestedJSON[titles] = selected;
    var otheroptions = {};
    var other = document.getElementById("someinfos");
    //alert(other);
    var tablesInsideDiv = other.getElementsByTagName("table");

    var ss = other.getElementsByTagName("input");
    for (i = 0; i < ss.length; i++) {
      if (ss[i].type != "checkbox") continue;
      if (ss[i].checked === true) {
        otheroptions[ss[i].name] = ss[i].value;
      }
    }
    var nest = {};

    for (var i = 0; i < tablesInsideDiv.length; i++) {
      var currentTable = tablesInsideDiv[i];
      var inputElements = currentTable.getElementsByTagName("input");
      var name = currentTable.id;
      var name = name.replace("_more_info", "");
      var othersolution = {};
      for (var j = 0; j < inputElements.length; j++) {
        if (inputElements[j].type != "checkbox") continue;
        if (inputElements[j].checked === true) {
          othersolution[inputElements[j].name] = inputElements[j].value;
        }

        nest[name] = othersolution;
      }
    }

    const removeEmpty = (obj) => {
      Object.keys(obj).forEach((key) => {
        if (obj[key] && typeof obj[key] === "object") {
          removeEmpty(obj[key]);

          if (Object.keys(obj[key]).length === 0) {
            delete obj[key];
          }
        } else if (!obj[key] && obj[key] !== undefined) {
          delete obj[key];
        }
      });

      if (Object.keys(obj).length === 0) {
        return undefined;
      }

      return obj;
    };

    nest = removeEmpty(nest);
    console.log(nestedJSON);

    selected = Object.assign(nestedJSON, nest);

    console.log(JSON.stringify(selected));
    selected = removeEmpty(selected);
  
    document.getElementById("viewpage").disabled = false;
    if (isEmpty(selected)) {

      alert("You haven't chose one  or more  checkboxes");
  }else{
    alert("Ola kala");
    sessionStorage.setItem("selected", JSON.stringify(selected));
    return selected;
  }
  }else{
    alert("You must select from dropdown your role");
  }
}
function isEmpty(obj) {
  for (let key in obj) {
      if (obj.hasOwnProperty(key)) {
          if (typeof obj[key] === 'object' && !isEmpty(obj[key])) {
              return false;
          } else if (typeof obj[key] !== 'object' || (Array.isArray(obj[key]) && obj[key].length > 0)) {
              return false;
          }
      }
  }
  return true;
}
function create_table(jsonData) {
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

  const tableContainer = document.getElementById("table-container");
  tableContainer.innerHTML = " ";
  tableContainer.appendChild(table);
}

function selectAll(value) {
  var selectElement = value;
  // alert(selectElement);

  var selectedOption = selectElement + "_info";
  var checkbox_all = document.getElementById(selectedOption);
  inputElements = checkbox_all.getElementsByTagName("input");
  for (i = 0; i < inputElements.length; i++) {
    if (inputElements[i].type != "checkbox") continue;
    inputElements[i].checked = true;
  }
}

function deselectAll(value) {
  var selectElement = value;
  var selectedOption = selectElement + "_info";
  var checkbox_all = document.getElementById(selectedOption);
  inputElements = checkbox_all.getElementsByTagName("input");
  for (i = 0; i < inputElements.length; i++) {
    if (inputElements[i].type != "checkbox") continue;
    inputElements[i].checked = false;
  }
}

function hasvalue() {
  var selectElement = document.getElementById("options");

  var selectedOption = selectElement.value + "_info";
  var checkbox_all = document.getElementById(selectedOption);
  if (checkbox_all === null) {
    return false;
  } else {
    return true;
  }
}
function removeall() {
  $("#someinfos div").empty();
}

function showpop() {
  var popwindow = document.getElementById("popup");
  popwindow.style.display = "block";
}
function closepopup() {
  var popwindow = document.getElementById("popup");
  popwindow.style.display = "none";
}
function submitpop() {
  var array = [];
  var popwindow = document.getElementById("popup");
  popwindow.style.display = "block";
  var checkboxes = document.querySelectorAll(
    " #popup input[type=checkbox]:checked"
  );

  for (var i = 0; i < checkboxes.length; i++) {
    array.push(checkboxes[i].value);
  }
  if (array.length != 0) {
    selected = generateinfo();

    if (Object.keys(selected).length === 0) {
      alert("You haven't choose one or more checkboxes");
    } else {
      for (var i = 0; i < array.length; i++) {
      if (array[i] === "json") {
          generatejson(selected);
          //create_table(selected);
        } else if (array[i] === "table") {
          alert("The data has exported suceessfuly");
          var buttonpage = document.getElementById("viewpage");
          buttonpage.removeAttribute("disabled");
        } else {
          alert("error");
        }
      }
      popwindow.style.display = "none";
      var title = document.getElementsByTagName("h5");

    }
  } else {
    alert("you must choose one option");
  }
}

function generatePDF(selected) {
  const doc = new jsPDF();

  Object.entries(selected).forEach((entry, index) => {
    const [key, value] = entry;
    console.log(`${key}: ${value}`);
    doc.text(`${key}: ${value}`, 5, 5 + index * 10);
  });
  doc.save("dataset_info_js.pdf");
}

function generatejson(selected) {
  var jsonString = JSON.stringify(selected, null, 4);

  var blob = new Blob([jsonString], { type: "application/json" });

  var a = document.createElement("a");

  a.download = "file.json";

  a.href = window.URL.createObjectURL(blob);

  document.body.appendChild(a);

  a.click();

  document.body.removeChild(a);
}
