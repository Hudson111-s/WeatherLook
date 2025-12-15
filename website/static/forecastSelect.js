document.addEventListener("DOMContentLoaded", () => {
    const forecastSelect = document.getElementById("forecastSelect");
    const allCurrent = document.querySelectorAll(".currentCheckboxesCol");
    const allForecast = document.querySelectorAll(".forecastCheckboxesCol");

    forecastSelect.addEventListener("change", () => {
        const isCurrent = forecastSelect.value === "&current=";
        allCurrent.forEach((checkbox) => checkbox.hidden = !isCurrent);
        allForecast.forEach((checkbox) => checkbox.hidden = isCurrent);
    });

    forecastSelect.dispatchEvent(new Event("change"));
});
