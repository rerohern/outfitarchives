
// _________________________________________________________________________________________________________________________________________________________
// closet piece sidebar + filtering _______________________________________________________________________________________________________________________
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