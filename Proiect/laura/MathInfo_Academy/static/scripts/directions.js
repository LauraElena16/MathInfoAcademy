function filterFunction(idSearchBar, idDropdown) {
    document.getElementById(idSearchBar).style.outline = '2px solid lightgray';
    let hiddenInput;
    if(idSearchBar == 'searchBar1') 
        hiddenInput = document.getElementById("start_node_input");
    else
        hiddenInput = document.getElementById("end_node_input");

    hiddenInput.value = "-1";
    console.log(hiddenInput)
    
    var input, filter, ul, li, a, i;
    input = document.getElementById(idSearchBar);
    filter = input.value.toUpperCase();
    div = document.getElementById(idDropdown);
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
        txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

function focusSearchBar(searchBarId) {
    setTimeout(function() {
        document.getElementById(searchBarId).nextElementSibling.style.display = 'block';
    }, 100);
}

function unfocusSearchBar(searchBarId) {
    setTimeout(function () {
        document.getElementById(searchBarId).nextElementSibling.style.display = 'none';
    }, 100);
}

function setStart(label, displayInfo){
    let hiddenInput = document.getElementById("start_node_input");
    hiddenInput.value = label;
    let startSearchbar = document.getElementById('searchBar1');
    startSearchbar.value = displayInfo;
    startSearchbar.style.outline = '3px solid green';
    console.log("inside setstart", label, hiddenInput)
}

function setDestination(label, displayInfo){
    let hiddenInput = document.getElementById("end_node_input");
    hiddenInput.value = label;
    let destSearchbar = document.getElementById('searchBar2');
    destSearchbar.value = displayInfo;
    destSearchbar.style.outline = '3px solid green';
    console.log("inside setdest", label, hiddenInput)
}


