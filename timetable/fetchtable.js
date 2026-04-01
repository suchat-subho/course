// 🔹 CONFIG
const jsonURL = "https://script.google.com/macros/s/AKfycbxHuQN2cdNuSABaSUd7Y3fLGLSgMEGdfJ-Rl0BCCrvhmF54zsgXW4QlDbIQsQgMhh98uQ/exec";

// 🔹 Modal helpers
function showLoading() {
  const modal = document.getElementById("loadingModal");
  //alert("Showing modal");
  modal.style.display = "flex";
  document.getElementById("loadingModal").classList.remove("hidden");
}

function hideLoading() {
  //alert("hideLoading called");
  document.getElementById("loadingModal").classList.add("hidden");
  modal.style.display = "none";
  
}

function highlightTodayRow() {
  const dayName = new Date().toLocaleString("en-US", {
    weekday: "long",
    timeZone: "Asia/Kolkata"
  });

  const rows = document.querySelectorAll("#timetable tr");

  rows.forEach(row => {
    if (row.cells[0] && row.cells[0].innerText === dayName) {
      row.classList.add("highlight");
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  showLoading();
  const start = Date.now();

  fetch(jsonURL)
    .then(res => res.json())
    .then(data => {
      buildTable(data);

      highlightTodayRow();   // 👈 ADD THIS HERE

      const elapsed = Date.now() - start;
      const delay = Math.max(500 - elapsed, 0);

      setTimeout(hideLoading, delay);
    })
    .catch(err => {
      console.error(err);
      hideLoading();
    });
});

function buildTable(data) {
  const table = document.getElementById("timetable");

  const days = Object.keys(data);

  if (days.length === 0) return;

  // 🔹 Extract time slots dynamically from first day
  const timeSlots = Object.keys(data[days[0]]);

  // 🔹 Header
  let header = "<tr><th>Day</th>";
  timeSlots.forEach(t => header += `<th>${t}</th>`);
  header += "</tr>";
  table.innerHTML = header;

  // 🔹 Rows
  days.forEach(day => {
    let rowHTML = `<tr><th>${day}</th>`;
    let slots = data[day];

    let i = 0;
    while (i < timeSlots.length) {
      let value = slots[timeSlots[i]];

      // Empty cell
      if (!value || value === "X") {
        rowHTML += `<td class="empty">X</td>`;
        i++;
        continue;
      }

      // 🔹 Merge consecutive identical slots
      let span = 1;
      while (
        i + span < timeSlots.length &&
        slots[timeSlots[i + span]] === value
      ) {
        span++;
      }

      let formatted = value.replace(/\n/g, " ").replace(/ /g, "<br>");
      rowHTML += `<td colspan="${span}">${formatted}</td>`;

      i += span;
    }

    rowHTML += "</tr>";
    table.innerHTML += rowHTML;
  });
}