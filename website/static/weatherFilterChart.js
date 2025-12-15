document.addEventListener("DOMContentLoaded", () => {
    const weatherSort = document.getElementById("weatherSort");
    const dateSort = document.getElementById("dateSort");
    const table = document.getElementById("weatherTable");
    const activeWeather = document.getElementById("activeWeather");
    const activeDate = document.getElementById("activeDate");
    const rows = table.querySelector("tbody").rows;
    
    const chartCtx = document.getElementById("weatherChart").getContext("2d");
    let weatherChart = null;

    const tableContainer = document.getElementById("tableContainer");
    const chartContainer = document.getElementById("chartContainer");

    function createChart(chartDataLabels, chartData) {
        if (weatherChart) {
            weatherChart.data.labels = chartDataLabels;
            weatherChart.data.datasets[0].data = chartData;
            weatherChart.data.datasets[0].label = activeWeather.textContent;
            weatherChart.update();
        } else {
            weatherChart = new Chart(chartCtx, {
            type: "line",
            data: {
                labels: chartDataLabels,
                datasets: [{label: activeWeather.textContent, data: chartData, borderColor: "rgba(75, 192, 192, 1)", fill: false}]
            },
            options: {responsive: true, scales: {y: {beginAtZero: false} }}
        });
        }
    }

    function destroyChartIfExists() {
        if (weatherChart) {
            weatherChart.destroy();
            weatherChart = null;
        }
    }

    function displaySortedWeather() {
        const chartDataLabels = [];
        const chartData = [];
        const weatherValue = weatherSort.value;
        const dateValue = dateSort.value;

        activeWeather.textContent = weatherValue === "All" ? "All Types" : weatherValue;
        activeDate.textContent = dateValue === "All" ? "All Dates" : dateValue;
              
        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].cells;
            const weatherType = cells[0].textContent.trim();
            const rowValue = parseFloat(cells[1].textContent.trim());
            const date = cells[2].textContent.trim();

            if ((date === dateValue || dateValue === "All") && (weatherType === weatherValue || weatherValue === "All")) {
                rows[i].hidden = false;

                if (weatherValue != "All" && dateValue == "All") {
                    chartDataLabels.push(date);
                    chartData.push(rowValue);
                }

            } else {
                rows[i].hidden = true;
            }
        }

        if (weatherValue !== "All" && dateValue === "All" && chartData.length > 1) {
            chartContainer.classList.remove("d-none");
            chartContainer.classList.add("col-md-6");
            tableContainer.classList.remove("col-md-12");
            tableContainer.classList.add("col-md-6");
            createChart(chartDataLabels, chartData);
        } else {
            chartContainer.classList.add("d-none");
            chartContainer.classList.remove("col-md-6");
            tableContainer.classList.add("col-md-12");
            tableContainer.classList.remove("col-md-6");
            destroyChartIfExists();
        }
    }

    weatherSort.addEventListener("change", displaySortedWeather);
    dateSort.addEventListener("change", displaySortedWeather);
    displaySortedWeather();
    
});
