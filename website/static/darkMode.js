document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");

    const setTheme = (isDark) => {
        if (isDark) {
            document.documentElement.setAttribute("data-bs-theme", "dark");
            themeIcon.classList.remove("bi-sun");
            themeIcon.classList.add("bi-moon");
            localStorage.setItem("theme", "dark");
        } else {
            document.documentElement.removeAttribute("data-bs-theme");
            themeIcon.classList.remove("bi-moon");
            themeIcon.classList.add("bi-sun");
            localStorage.setItem("theme", "light");
        }
        toggle.checked = isDark;
    };

    const savedTheme = localStorage.getItem("theme");
    setTheme(savedTheme === "dark");

    toggle.addEventListener("change", () => setTheme(toggle.checked));
});
