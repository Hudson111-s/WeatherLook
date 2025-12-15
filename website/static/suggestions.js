document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("locationInput");
    const suggestions = document.getElementById("suggestions");

    let debounceTimeout;

    input.addEventListener("input", () => {
        const q = input.value.trim();
        clearTimeout(debounceTimeout);

        if (q.length < 3) {
            suggestions.innerHTML = "";
            suggestions.hidden = true;
            return;
        }

        debounceTimeout = setTimeout(() => {
            fetch(`/autocomplete?q=${encodeURIComponent(q)}`)
            .then(response => response.json())
            .then(data => { 

                suggestions.innerHTML = "";

                if (data.length <= 0) return;

                data.forEach(location => {
                    const item = document.createElement("div");
                    item.classList.add("suggestion-item");
                    item.textContent = location;

                    item.addEventListener("click", () => {
                        input.value = location;
                        suggestions.innerHTML = "";
                        suggestions.hidden = true;
                    });

                    suggestions.appendChild(item);
                });
                suggestions.hidden = false;
            });
        }, 300);
    });

    document.addEventListener("click", (e) => {
        if (!input.contains(e.target) && !suggestions.contains(e.target)) {
            suggestions.innerHTML = "";
            suggestions.hidden = true;
        }
    });

});