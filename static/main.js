
// _________________________________________________________________________________________________________________________________________________________
// closet piece sidebar + filtering 
// _________________________________________________________________________________________________________________________________________________________

// sidebar hover handling
const sidebar = document.querySelector(".closet-sidebar")

sidebar.addEventListener('mouseenter', () => {
    sidebar.classList.add('expanded');
});

sidebar.addEventListener('mouseleave', () => {
    sidebar.classList.remove('expanded');
});

// closet item search and filter
document.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelectorAll('.closet-piece-container');
    const buttons = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('closet-search-input');

    let activeCategory = null;

    function filterItems() {
        const query = searchInput?.value?.toLowerCase() || '';

        items.forEach(item => {
            const name = item.dataset.name || '';
            const brand = item.dataset.brand || '';
            const category = item.dataset.category || '';

            const matchesSearch =
                name.includes(query) ||
                brand.includes(query);

            const matchesCategory =
                !activeCategory || category === activeCategory;

            const shouldHide = !(matchesSearch && matchesCategory);

            item.classList.toggle('hidden', shouldHide);
        });
    }

    // 🔍 SEARCH
    if (searchInput) {
        searchInput.addEventListener('input', filterItems);
    }

    // 🏷️ FILTER BUTTONS
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const selected = button.dataset.category;

            if (selected === 'all') {
                // always reset everything
                activeCategory = null;
            } else {
                // toggle behavior for categories
                activeCategory =
                    activeCategory === selected ? null : selected;
            }

            filterItems();
        });
    });
});

// _________________________________________________________________________________________________________________________________________________________
//  Log Outfit Forms | Drag + Drop Outfit Media 
// _________________________________________________________________________________________________________________________________________________________


const dragDropArea = document.getElementById("drag-drop-area");
const fileInput = document.getElementById("file-input");
const previewContainer = document.getElementById("preview-container");
const mediaDataInput = document.getElementById("media-data");

let mediaFiles = [];

// Open file picker
dragDropArea.addEventListener("click", () => fileInput.click());

// Drag events
dragDropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dragDropArea.classList.add("dragover");
});

dragDropArea.addEventListener("dragleave", () => {
    dragDropArea.classList.remove("dragover");
});

dragDropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dragDropArea.classList.remove("dragover");
    handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener("change", () => handleFiles(fileInput.files));

function handleFiles(files) {
    for (const file of files) {
        if (!file.type.startsWith("image/")) continue;

        const reader = new FileReader();

        reader.onload = (e) => {
            const previewItem = document.createElement("div");
            previewItem.classList.add("preview-item");

            // Image preview
            const img = document.createElement("img");
            img.src = e.target.result;

            // Alt text
            const altInput = document.createElement("input");
            altInput.placeholder = "Alt text";

            // Media type
            const typeSelect = document.createElement("select");
            ["outfit", "outfit_alt", "detail"].forEach(type => {
                const option = document.createElement("option");
                option.value = type;
                option.text = type;
                typeSelect.appendChild(option);
            });

            // View (IMPORTANT for your model)
            const viewSelect = document.createElement("select");
            ["Front", "Side", "Back", "Detail"].forEach(view => {
                const option = document.createElement("option");
                option.value = view;
                option.text = view;
                viewSelect.appendChild(option);
            });

            // Remove button
            const removeBtn = document.createElement("button");
            removeBtn.textContent = "Remove";

            removeBtn.addEventListener("click", () => {
                previewItem.remove();
                mediaFiles = mediaFiles.filter(m => m.file !== file);
                updateMediaData();
            });

            // Update on change
            [altInput, typeSelect, viewSelect].forEach(el => {
                el.addEventListener("input", updateMediaData);
            });

            previewItem.append(img, altInput, typeSelect, viewSelect, removeBtn);
            previewContainer.appendChild(previewItem);

            mediaFiles.push({
                file,
                altInput,
                typeSelect,
                viewSelect
            });

            updateMediaData();
        };

        reader.readAsDataURL(file);
    }
}

// Convert to JSON for backend
function updateMediaData() {
    const outfitCode = generateOutfitCode(); // you can replace this if backend generates it

    const mediaData = mediaFiles.map(item => ({
        img_src: `/static/media/outfits/${outfitCode}/${item.file.name}`,
        alt_text: item.altInput.value,
        media_type: item.typeSelect.value,
        view: item.viewSelect.value
    }));

    mediaDataInput.value = JSON.stringify(mediaData);
}

// TEMP helper (or remove if backend handles code)
function generateOutfitCode() {
    const date = document.querySelector('input[name="date_worn"]').value;
    return date || "temp";
}