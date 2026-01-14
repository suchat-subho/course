document.addEventListener("DOMContentLoaded", function () {

    const menuBtn = document.getElementById("menuBtn");
    const modal = document.getElementById("classModal");
    const closeBtn = document.querySelector(".close");
    const classList = document.getElementById("classList");

    menuBtn.addEventListener("click", function () {

        const table = document.querySelector("table");
        const rows = table.rows;

        const times = Array.from(rows[0].cells)
            .slice(1)
            .map(cell => cell.innerText.trim());

        classList.innerHTML = "";

        const schedule = {};   // { Monday: [ "11:20–1:00 PCS217", ... ] }

        for (let i = 1; i < rows.length; i++) {
            const day = rows[i].cells[0].innerText.trim();
            let timeIndex = 0;

            schedule[day] = [];

            for (let j = 1; j < rows[i].cells.length; j++) {
                const cell = rows[i].cells[j];
                const colspan = cell.colSpan || 1;
                const text = cell.innerText.trim();

                if (text && text !== "X") {
                    const start = times[timeIndex].split("-")[0];
                    const end = times[timeIndex + colspan - 1].split("-")[1];
                    schedule[day].push(
                        `${start}-${end} ${text.replace(/\n/g, " ")}`
                    );

                    //const startTime = times[timeIndex];
                    //const endTime = times[timeIndex + colspan - 1];

                    //schedule[day].push(
                    //    `${startTime}–${endTime} ${text.replace(/\n/g, " ")}`
                    //);
                }
                timeIndex += colspan;
            }
        }

        // Render day-wise single line
        for (const day in schedule) {
            if (schedule[day].length > 0) {
                const li = document.createElement("li");
                li.innerHTML = `
                    <strong>${day}:</strong>
                    ${schedule[day].join(" | ")}
                `;
                classList.appendChild(li);
            }
        }

        modal.style.display = "block";
    });

    closeBtn.onclick = () => modal.style.display = "none";

    window.onclick = (e) => {
        if (e.target === modal) modal.style.display = "none";
    };

});
