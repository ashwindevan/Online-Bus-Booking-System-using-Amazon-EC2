function myMenuFunction() {
    var i = document.getElementById("navMenu");
    if (i.className === "nav-menu") {
        i.className += " responsive";
    } else {
        i.className = "nav-menu";
    }
}

function ourroutes() {
    console.log("Our Routes button clicked.");
    fetch('/routes')
        .then(response => response.json())
        .then(routes => {
            console.log("Routes data fetched:", routes);
            var tableBody = document.getElementById("routesTableBody");
            tableBody.innerHTML = "";

            routes.forEach(route => {
                var row = document.createElement("tr");

                var fromCell = document.createElement("td");
                fromCell.textContent = route.from;
                row.appendChild(fromCell);

                var toCell = document.createElement("td");
                toCell.textContent = route.to;
                row.appendChild(toCell);

                var timingsCell = document.createElement("td");
                timingsCell.textContent = route.timings;
                row.appendChild(timingsCell);

                var distanceCell = document.createElement("td");
                distanceCell.textContent = route.distance;
                row.appendChild(distanceCell);

                tableBody.appendChild(row);
            });

            document.getElementById("routesModal").style.display = "block";
        })
        .catch(error => {
            console.error('Error fetching routes:', error);
            alert('Failed to fetch routes. Please try again later.');
        });
}

function closeModal() {
    document.getElementById("routesModal").style.display = "none";
    document.getElementById("bookingModal").style.display = "none";
}

function populateDropdowns() {
    fetch('/routes')
        .then(response => response.json())
        .then(routes => {
            const fromSelect = document.getElementById("fromSelect");
            const toSelect = document.getElementById("toSelect");

            fromSelect.innerHTML = "";
            toSelect.innerHTML = "";

            const uniquePlaces = new Set();
            routes.forEach(route => {
                uniquePlaces.add(route.from);
                uniquePlaces.add(route.to);
            });

            uniquePlaces.forEach(place => {
                const fromOption = new Option(place, place);
                const toOption = new Option(place, place);
                fromSelect.appendChild(fromOption);
                toSelect.appendChild(toOption);
            });

            fromSelect.addEventListener('change', updateToDropdown);
            toSelect.addEventListener('change', updateFromDropdown);
        })
        .catch(error => {
            console.error('Error fetching routes:', error);
            alert('Failed to fetch routes. Please try again later.');
        });
}

function updateToDropdown() {
    const fromValue = document.getElementById("fromSelect").value;
    const toSelect = document.getElementById("toSelect");
    const options = Array.from(toSelect.options);
    toSelect.innerHTML = "";
    options.forEach(option => {
        if (option.value !== fromValue) {
            toSelect.add(option);
        }
    });
}

function updateFromDropdown() {
    const toValue = document.getElementById("toSelect").value;
    const fromSelect = document.getElementById("fromSelect");
    const options = Array.from(fromSelect.options);
    fromSelect.innerHTML = "";
    options.forEach(option => {
        if (option.value !== toValue) {
            fromSelect.add(option);
        }
    });
}

function showCalendar() {
    const dateInput = document.getElementById("dateInput");
    const today = new Date();
    const nextWeek = new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000);

    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    dateInput.min = formatDate(today);
    dateInput.max = formatDate(nextWeek);
    dateInput.disabled = false; // Enable the date input field
}

function bookTickets() {
    populateDropdowns();
    showCalendar();
    document.getElementById("bookingModal").style.display = "block";
}

document.getElementById('bookingForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const from = document.getElementById('fromSelect').value;
    const to = document.getElementById('toSelect').value;
    const date = document.getElementById('dateInput').value;

    fetch('/book_tickets', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `from=${from}&to=${to}&date=${date}`
    }).then(response => response.json())
      .then(data => {
          alert(data.message);
      })
      .catch(error => {
          console.error('Error:', error);
      });

    document.getElementById('bookingModal').style.display = 'none';
});

function logout() {
    fetch('/logout', {
        method: 'GET',
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url; // Redirect to the login page
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}

// Call populateDropdowns() when the page loads
window.onload = populateDropdowns;

// Close modal when clicking outside of it
window.onclick = function(event) {
    var modal = document.getElementById("routesModal");
    var bookingModal = document.getElementById("bookingModal");
    if (event.target == modal || event.target == bookingModal) {
        modal.style.display = "none";
        bookingModal.style.display = "none";
    }
}
