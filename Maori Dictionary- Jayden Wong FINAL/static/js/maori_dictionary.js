
// code to highlight table words
// makes table rows with the class "clickable-row" be highlighted on users screen.
jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});

// Code for search functio
function search_function() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("search_function");
  filter = input.value.toUpperCase();
  table = document.getElementById("search_table");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

// code to sort words alphabetically or numerically by clicking on table header.
function sort_function(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("dictionary_table");
switching = true;
 // Set the sorting direction to ascending:
dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.getElementsByTagName("TR");
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
        // Start by saying there should be no switching:
        shouldSwitch = false;
             /* Get the two elements you want to compare,
      one from current row and one from the next: */
        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 1].getElementsByTagName("TD")[n];
        // compares string if there is no number
                var cmpX=isNaN(parseInt(x.innerHTML))?x.innerHTML.toLowerCase():parseInt(x.innerHTML);
                var cmpY=isNaN(parseInt(y.innerHTML))?y.innerHTML.toLowerCase():parseInt(y.innerHTML);
cmpX=(cmpX=='-')?0:cmpX;
cmpY=(cmpY=='-')?0:cmpY;
        if (dir == "asc") {
            if (cmpX > cmpY) {
                shouldSwitch= true;
                // If so, mark as a switch and break the loop:
                break;
            }
        } else if (dir == "desc") {
            if (cmpX < cmpY) {
                shouldSwitch= true;
                // If so, mark as a switch and break the loop:
                break;
            }
        }
    }
    if (shouldSwitch) {
              /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        // Each time a switch is done, increase this count by 1:
        switchcount ++;
    } else {
        if (switchcount == 0 && dir == "asc") {
            dir = "desc";
            switching = true;
        }
    }
}
}

// Confirm delete
$('.confirmation').on('click', function () {
return confirm('Are you sure?');
});

// Remove error message
function removeAlert() { //when the "X" is clicked on, error is removed.
    console.log('clicked'); // outputs message to console.
    $(this).parent().parent().remove();
}

$('.alert-close>a').on('click', removeAlert); // on click, alert is removed.