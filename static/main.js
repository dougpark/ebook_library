// Auto-hide flash messages

window.addEventListener("DOMContentLoaded", () => {
    const flashes = document.querySelectorAll(".flash");

    if (flashes.length > 0) {
        setTimeout(() => {
            flashes.forEach(flash => {
                flash.style.opacity = "0";
                setTimeout(() => flash.remove(), 500);
            });
        }

            , 3000);
    }

    let selectedCategory = "";
    const searchBox = document.getElementById("searchBox");
    const clearBtn = document.getElementById("clearSearch");
    const categoryLinks = document.querySelectorAll(".category-link");

    // Search/filter logic
    function filterCards(filter, category) {
        const cards = document.querySelectorAll(".ebook-card");
        cards.forEach(card => {
            const title = card.querySelector(".ebook-title").innerText.toLowerCase();
            const author = card.querySelector(".ebook-author").innerText.toLowerCase();
            const date = card.querySelector(".ebook-date").innerText.toLowerCase();
            const categoryText = card.querySelector(".ebook-category")
                ? card.querySelector(".ebook-category").innerText.toLowerCase()
                : "";
            const notes = card.querySelector(".ebook-notes")
                ? card.querySelector(".ebook-notes").innerText.toLowerCase()
                : "";

            const matchesFilter =
                title.includes(filter) ||
                author.includes(filter) ||
                date.includes(filter) ||
                categoryText.includes(filter) ||
                notes.includes(filter);

            const matchesCategory =
                !category || category === "all" || categoryText === category;

            card.style.display = (matchesFilter && matchesCategory) ? "" : "none";
        });
    }

    function refreshCategoryList() {
        fetch('/categories')
            .then(response => response.json())
            .then(categories => {
                const categoryList = document.getElementById('categoryList');
                categoryList.innerHTML = '<li><a href="#" class="category-link">All</a></li>';
                categories.forEach(category => {
                    const li = document.createElement('li');
                    li.innerHTML = `<a href="#" class="category-link">${category}</a>`;
                    categoryList.appendChild(li);
                });

                // Re-attach click event listeners to new category links
                const newCategoryLinks = categoryList.querySelectorAll('.category-link');
                newCategoryLinks.forEach(link => {
                    link.addEventListener("click", function (e) {
                        e.preventDefault();
                        selectedCategory = this.textContent.trim().toLowerCase();
                        filterCards(searchBox.value.toLowerCase(), selectedCategory);

                        // Highlight selected category
                        newCategoryLinks.forEach(l => l.classList.remove("selected"));
                        this.classList.add("selected");
                    });
                });
            });
    }

    // Search box event
    searchBox.addEventListener("keyup", function () {
        const filter = this.value.toLowerCase();
        filterCards(filter, selectedCategory);
    });

    // Clear button event
    clearBtn.addEventListener("click", function () {
        searchBox.value = "";
        searchBox.dispatchEvent(new Event("keyup"));
        searchBox.focus();
    });

    // Category click event
    categoryLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            selectedCategory = this.textContent.trim().toLowerCase();
            filterCards(searchBox.value.toLowerCase(), selectedCategory);

            // Optional: highlight selected category
            categoryLinks.forEach(l => l.classList.remove("selected"));
            this.classList.add("selected");
        });
    });

    // Initial filter
    filterCards("", "");



    document.querySelectorAll('.ebook-card').forEach(card => {
        const saveBtn = card.querySelector('.save-btn');
        saveBtn.disabled = true; // Start disabled

        const editableFields = card.querySelectorAll('.editable');
        editableFields.forEach(field => {
            field.addEventListener('input', () => {
                saveBtn.disabled = false;
            });
        });

        saveBtn.addEventListener('click', function () {
            const code = card.dataset.code;
            const title = card.querySelector('.ebook-title').innerText.trim();
            const author = card.querySelector('.ebook-author').innerText.trim();
            const date = card.querySelector('.ebook-date').innerText.trim();
            const category = card.querySelector('.ebook-category')
                ? card.querySelector('.ebook-category').innerText.trim()
                : "";
            const notes = card.querySelector('.ebook-notes')
                ? card.querySelector('.ebook-notes').innerText.trim()
                : "";

            fetch('/update_metadata', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    code,
                    title,
                    author,
                    date,
                    category,
                    notes
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        saveBtn.textContent = 'Saved!';
                        setTimeout(() => saveBtn.textContent = 'Save', 1500);
                        saveBtn.disabled = true; // Disable again after save
                        refreshCategoryList(); // Refresh category list after save
                    } else {
                        saveBtn.textContent = 'Error!';
                        setTimeout(() => saveBtn.textContent = 'Save', 1500);
                    }
                })
                .catch(() => {
                    saveBtn.textContent = 'Error!';
                    setTimeout(() => saveBtn.textContent = 'Save', 1500);
                });
        });
    });
});

// Table sorting function (same as before)
function sortTable(n) {
    const table = document.getElementById("ebookTable");
    let rows,
        switching,
        i,
        x,
        y,
        shouldSwitch,
        dir,
        switchcount = 0;
    switching = true;
    dir = "asc";

    while (switching) {
        switching = false;
        rows = table.rows;

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];

            if (dir === "asc") {
                if (x.textContent.toLowerCase() > y.textContent.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }

            else if (dir === "desc") {
                if (x.textContent.toLowerCase() < y.textContent.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }
        }

        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        }

        else {
            if (switchcount === 0 && dir === "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

function showFlash(message, category) {
    const flashDiv = document.createElement("div");
    flashDiv.className = `flash ${category}`;
    flashDiv.textContent = message;
    flashDiv.style.position = "fixed";
    flashDiv.style.top = "20px";
    flashDiv.style.right = "20px";
    flashDiv.style.zIndex = "9999";
    flashDiv.style.padding = "10px 20px";
    flashDiv.style.background =
        category === "success" ? "#4caf50" :
            category === "error" ? "#f44336" :
                "#2196f3"; // default to blue for info
    flashDiv.style.color = "#fff";
    flashDiv.style.borderRadius = "4px";
    flashDiv.setAttribute("role", "alert");
    document.body.appendChild(flashDiv);

    setTimeout(() => {
        flashDiv.style.opacity = "0";
        setTimeout(() => flashDiv.remove(), 500);
    }, 3000);
}

function sortEbooks(byField) {
    // Get all ebook cards
    const cards = Array.from(document.querySelectorAll('.ebook-card'));
    cards.sort((a, b) => {
        const aVal = a.querySelector(`.ebook-${byField}`).textContent.trim().toLowerCase();
        const bVal = b.querySelector(`.ebook-${byField}`).textContent.trim().toLowerCase();
        return aVal.localeCompare(bVal);
    });
    const list = document.getElementById('ebookList');
    cards.forEach(card => list.appendChild(card)); // Re-append in sorted order
}

// Example usage: sortEbooks('title');

document.getElementById("openSidebar").addEventListener("click", function () {
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("mainContent");
    sidebar.classList.add("active");
    sidebar.classList.remove("closed");
    mainContent.classList.remove("sidebar-closed");
});

document.getElementById("closeSidebar").addEventListener("click", function () {
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("mainContent");
    sidebar.classList.remove("active");
    sidebar.classList.add("closed");
    mainContent.classList.add("sidebar-closed");
});

// Optional: close sidebar when clicking outside (mobile UX)
document.addEventListener("click", function (e) {
    const sidebar = document.getElementById("sidebar");
    const openBtn = document.getElementById("openSidebar");
    if (
        sidebar.classList.contains("active") &&
        !sidebar.contains(e.target) &&
        e.target !== openBtn &&
        window.innerWidth <= 700
    ) {
        sidebar.classList.remove("active");
    }
});