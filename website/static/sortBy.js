document.addEventListener("DOMContentLoaded", () => {
    const weatherSort = document.getElementById("weatherSort");
    const dateSort = document.getElementById("dateSort");
    const table = document.getElementById("weatherTable");
    const activeWeather = document.getElementById("activeWeather");
    const activeDate = document.getElementById("activeDate");
    const rows = table.querySelector("tbody").rows;
    
    const chartCtx = document.getElementById('weatherChart').getContext('2d');
    let weatherChart = null;

    const tableContainer = document.getElementById("tableContainer");
    const graphContainer = document.getElementById("chartContainer");

    function create_graph(chartDataLabels, chartData) {
        if (weatherChart) {
            weatherChart.data.labels = chartDataLabels;
            weatherChart.data.datasets[0].data = chartData;
            weatherChart.data.datasets[0].label = activeWeather.textContent;
            weatherChart.update();
        } else {
            weatherChart = new Chart(chartCtx, {
            type: 'line',
            data: {
                labels: chartDataLabels,
                datasets: [{label: activeWeather.textContent, data: chartData, borderColor: 'rgba(75, 192, 192, 1)', fill: false}]
            },
            options: {responsive: true, scales: {y: {beginAtZero: false} }}
        });
        }
    }

    function displaySortedWeather() {
        const chartDataLabels = [];
        const chartData = [];
        const weatherValue = weatherSort.value;
        const dateValue = dateSort.value;

        activeWeather.textContent = weatherValue == "All" ? "All Types" : weatherValue;
        activeDate.textContent = dateValue == "All" ? "All Dates" : dateValue;
              
        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].cells;
            const weatherType = cells[0].textContent.trim();
            const rowValue = parseFloat(cells[1].textContent.trim());
            const date = cells[2].textContent.trim();

            if ((date === dateValue || dateValue === "All") && (weatherType === weatherValue || weatherValue === "All")) {
                rows[i].style.display = "";

                if (weatherValue != "All" && dateValue == "All") {
                    chartDataLabels.push(date);
                    chartData.push(rowValue);
                }

            } else {
                rows[i].style.display = "none";
            }
        }

        if (weatherValue != "All" && dateValue == "All") {
            graphContainer.classList.remove("d-none");
            graphContainer.classList.add("col-md-6");
            tableContainer.classList.remove("col-md-12");
            tableContainer.classList.add("col-md-6");
            create_graph(chartDataLabels, chartData);
        } else {
            graphContainer.classList.add("d-none");
            graphContainer.classList.remove("col-md-6");
            tableContainer.classList.add("col-md-12");
            tableContainer.classList.remove("col-md-6");
        }
    }

    weatherSort.addEventListener("change", displaySortedWeather);
    dateSort.addEventListener("change", displaySortedWeather);
    displaySortedWeather();
    
});
