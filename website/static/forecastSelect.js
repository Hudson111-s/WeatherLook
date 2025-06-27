document.addEventListener("DOMContentLoaded", () => {
    const forecastSelect = document.getElementById("forecastSelect");

    forecastSelect.addEventListener("change", () => {
        const forecastValue = forecastSelect.value;
        const allCurrent = document.querySelectorAll(".currentCheckboxesCol");
        const allForecast = document.querySelectorAll(".forecastCheckboxesCol");

        if (forecastValue === "&current=") {
            allCurrent.forEach((checkbox) => {checkbox.style.display = "block"; });
            allForecast.forEach((checkbox) => {checkbox.style.display = "none"; });
        } else {
            allCurrent.forEach((checkbox) => {checkbox.style.display = "none"; });
            allForecast.forEach((checkbox) => {checkbox.style.display = "block"; });
        }
    });

    forecastSelect.dispatchEvent(new Event("change"));
});
