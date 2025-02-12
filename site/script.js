document.addEventListener("DOMContentLoaded", () => {
    let sourcesPath = "https://raw.githubusercontent.com/majidrezarahnavard/way_of_freedom_media/main/source/";
    document.getElementById("search-btn").addEventListener("click", async (event) => {
        event.preventDefault();
        let searchValue = document.getElementById("search-value").value || "*";
        let searchType = document.getElementById("search-type").value || "title";
        let reSourceType = "";
        try {
            let response = await fetch("all.json");
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            reSourceType = await response.json();
            reSourceType = reSourceType[searchType];
        } catch (error) {
            console.error("Error fetching data:", error);
        };
        let filteredData = reSourceType.filter(item => {
            let fieldValue = item[searchType]?.toString().toLowerCase() || "";
            let query = searchValue.toLowerCase();

            return searchValue === "*" || fieldValue.includes(query);
        });
        displayResults(filteredData)
    });
    function displayResults(data) {
        let resultsContainer = document.getElementById("sources");
        resultsContainer.innerHTML = "";

        if (data.length === 0) {
            resultsContainer.innerHTML = "<p>هیچ نتیجه‌ای پیدا نشد.</p>";
            return;
        }

        let list = document.createElement("ul");
        list.classList.add("list-group");

        data.forEach(item => {
            let listItem = document.createElement("li");
            listItem.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");

            let textSpan = document.createElement("span");
            textSpan.textContent = `${item.title} - ${item.description}`;

            let viewButton = document.createElement("a");
            viewButton.classList.add("btn", "btn-primary", "btn-sm");
            viewButton.textContent = "مشاهده";
            viewButton.href = sourcesPath + item.file;
            viewButton.target = "_blank";

            let copyButton = document.createElement("button");
            copyButton.classList.add("btn", "btn-secondary", "btn-sm", "ms-2");
            copyButton.textContent = "کپی لینک";
            copyButton.addEventListener("click", () => {
                navigator.clipboard.writeText(item.file).then(() => {
                    alert("لینک کپی شد!");
                }).catch(err => console.error("خطا در کپی لینک:", err));
            });

            let buttonContainer = document.createElement("div");
            buttonContainer.appendChild(viewButton);
            buttonContainer.appendChild(copyButton);

            listItem.appendChild(textSpan);
            listItem.appendChild(buttonContainer);
            list.appendChild(listItem);
        });

        resultsContainer.appendChild(list);
    }

});
