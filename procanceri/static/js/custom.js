function handleRowClick(run_id, name, run_info){
    run_info = JSON.parse(run_info);
    console.log(name);
  
    // Create a new table with Bootstrap classes and a custom class for centering
    var table = $('<table>').attr('class', 'table thead-dark table-striped');
    var thead = $('<thead>').attr('class', 'thead-dark', 'text-center');
    // Add a table header row with Bootstrap classes
    var headerRow = $('<tr>').attr('class', 'thead-light');
    headerRow.append($('<th>').text(name));
    headerRow.append($('<th>').text(''));
    thead.append(headerRow);
    table.append(thead);
  
    let tbody = $('<tbody>');
    // Add rows to the table for each key-value pair in the run_info object
    $.each(run_info, function(key, value) {
        addTableRow(tbody, key, value);
    });
    table.append(tbody);
  
    // Remove any existing table in the container element
    $('#my-container').empty(); 
    // Add the new table to the container element and center it
    $('#my-container').addClass('text-center').append(table);
    
    // Remove the click event from the rows in the first table to prevent the new table from disappearing
    $('#pipeline-table tbody tr').off('click');
  }
//   function addTableRow(table, key, value) {
//     // Create a new row and add it to the table
//     var row = $('<tr>');
//     table.append(row);

//         // Add the key and value as separate cells in the row
//         row.append($('<td>').text(key));
//         row.append($('<td>').text(value));
 

//         if(typeof value === 'object') {
//             // If the value is an object, add a nested table to display its contents
//             var nestedTable = $('<table>').attr('class', 'table thead-dark table-striped');
//             row.append($('<td>').append(nestedTable));
//             $.each(value, function(subkey, subvalue) {
//                 addTableRow(nestedTable, subkey, subvalue);
//             });
//         }
//     }
function showTable(stage) {
  console.log(stage);
  var tables = document.querySelectorAll("#tableContainer table");
  alert("nai");

  tables.forEach(function(table) {
    if (table.id === stage) {
      table.classList.remove("hidden");
    } else {
      table.classList.add("hidden");
    }
  });
}

$(document).ready(function() {
  if ($(window).width() <= 767) {
      $(".arrow-icon").addClass("mobile");
  } else {
      $(".arrow-icon").addClass("desktop");
  }
});

window.addEventListener("scroll", function() {
  var scrollButton = document.getElementById("scroll-to-top");
  
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    scrollButton.style.display = "block";
  } else {
    scrollButton.style.display = "none";
  }
});

function scrollToTop() {
  document.body.scrollTop = 0;    // For Safari
  document.documentElement.scrollTop = 0;    // For Chrome, Firefox, IE, and Opera
}

var scrollButton = document.getElementById("scroll-to-top");
scrollButton.addEventListener("click", scrollToTop);
