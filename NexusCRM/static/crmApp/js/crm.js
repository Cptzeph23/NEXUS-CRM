document.addEventListener("DOMContentLoaded", function () {

    const sidebarToggle = document.getElementById("sidebarToggle");
    const sidebar = document.querySelector(".crm-sidebar");

    if (sidebarToggle && sidebar) {

        sidebarToggle.addEventListener("click", function () {

            const isOpen = sidebar.classList.toggle("open");
            sidebarToggle.setAttribute("aria-expanded", String(isOpen));

        });

    }


    /*
     * Automatically dismiss Django messages.
     */

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            const closeButton = alert.querySelector(".btn-close");

            if (closeButton) {
                closeButton.click();
            }

        }, 5000);

    });


    /*
     * Keyboard shortcut:
     * "/" focuses the global search.
     */

    document.addEventListener("keydown", function (event) {

        if (
            event.key === "/" &&
            !["INPUT", "TEXTAREA", "SELECT"].includes(
                document.activeElement.tagName
            )
        ) {

            event.preventDefault();

            const searchInput =
                document.querySelector(".topbar-search input");

            if (searchInput) {
                searchInput.focus();
            }

        }

    });

});
