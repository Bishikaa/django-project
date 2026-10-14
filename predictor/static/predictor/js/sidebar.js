function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    if (!dropdown) return;
    
    // Close other dropdowns
    document.querySelectorAll('.topbar-dropdown.open, .dropdown.open').forEach(d => {
        if (d.id !== id) d.classList.remove('open');
    });

    dropdown.classList.toggle('open');
}

document.addEventListener('click', function(e) {
    if (!e.target.closest('.topbar-dropdown') && !e.target.closest('.dropdown')) {
        document.querySelectorAll('.topbar-dropdown.open, .dropdown.open').forEach(d => d.classList.remove('open'));
    }
});

function toggleAccountSettings() {
    const container = document.getElementById('accountSettingsContainer');
    if (container.style.display === 'none') {
        container.style.display = 'grid';
        container.scrollIntoView({ behavior: 'smooth' });
    } else {
        container.style.display = 'none';
    }
}
