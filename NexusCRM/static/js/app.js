document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("crmSidebar");
    const menuButton = document.getElementById("mobileMenuButton");
    const overlay = document.getElementById("sidebarOverlay");


    /*
    ========================================
    MOBILE SIDEBAR
    ========================================
    */

    if (menuButton && sidebar && overlay) {

        menuButton.addEventListener("click", function () {

            sidebar.classList.toggle("mobile-open");

            overlay.classList.toggle("active");

        });


        overlay.addEventListener("click", function () {

            sidebar.classList.remove("mobile-open");

            overlay.classList.remove("active");

        });

    }


    /*
    ========================================
    GLOBAL SEARCH SHORTCUT
    ========================================
    */

    document.addEventListener("keydown", function (event) {

        if (
            event.key === "/" &&
            document.activeElement.tagName !== "INPUT" &&
            document.activeElement.tagName !== "TEXTAREA"
        ) {

            const search =
                document.querySelector(
                    '.global-search input'
                );

            if (search) {

                event.preventDefault();

                search.focus();

            }

        }

    });


    /*
    ========================================
    CONSOLE CHECK
    ========================================
    */

    console.log(
        "NexusCRM application shell loaded successfully."
    );

});