/* =========================================================
   JNAIVA — GLOBAL JAVASCRIPT
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       MOBILE NAVIGATION
    ===================================================== */

    const menuToggle =
        document.querySelector(".menu-toggle");

    const mainNav =
        document.querySelector(".main-nav");

    if (menuToggle && mainNav) {

        menuToggle.addEventListener("click", () => {

            mainNav.classList.toggle("open");

            const isOpen =
                mainNav.classList.contains("open");

            menuToggle.setAttribute(
                "aria-expanded",
                isOpen
            );

            menuToggle.textContent =
                isOpen ? "×" : "☰";
        });


        /* Close menu after clicking a link */

        mainNav
            .querySelectorAll("a")
            .forEach(link => {

                link.addEventListener("click", () => {

                    mainNav.classList.remove("open");

                    menuToggle.textContent = "☰";

                    menuToggle.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                });

            });
    }


    /* =====================================================
       HEADER SCROLL EFFECT
    ===================================================== */

    const header =
        document.querySelector(".site-header");

    const updateHeader = () => {

        if (!header) return;

        if (window.scrollY > 20) {

            header.style.boxShadow =
                "0 8px 30px rgba(0,0,0,.045)";

        } else {

            header.style.boxShadow =
                "none";
        }
    };

    updateHeader();

    window.addEventListener(
        "scroll",
        updateHeader,
        { passive: true }
    );


    /* =====================================================
       SCROLL REVEAL
    ===================================================== */

    const revealElements =
        document.querySelectorAll(".reveal");

    if (revealElements.length) {

        const revealObserver =
            new IntersectionObserver(
                entries => {

                    entries.forEach(entry => {

                        if (entry.isIntersecting) {

                            entry.target.classList.add(
                                "visible"
                            );

                            revealObserver.unobserve(
                                entry.target
                            );
                        }

                    });

                },
                {
                    threshold: 0.12
                }
            );

        revealElements.forEach(element => {

            revealObserver.observe(element);

        });
    }


    /* =====================================================
       SMOOTH INTERNAL LINKS
    ===================================================== */

    document
        .querySelectorAll('a[href^="#"]')
        .forEach(link => {

            link.addEventListener("click", event => {

                const targetId =
                    link.getAttribute("href");

                if (
                    !targetId ||
                    targetId === "#"
                ) {
                    event.preventDefault();
                    return;
                }

                const target =
                    document.querySelector(targetId);

                if (!target) return;

                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            });

        });


    /* =====================================================
       DEMO MODAL
    ===================================================== */

    const demoButtons =
        document.querySelectorAll(
            '[data-demo], .watch-demo'
        );

    const modal =
        document.querySelector(
            ".modal-overlay"
        );

    const closeModal =
        document.querySelector(
            ".modal-close"
        );

    const openDemo = () => {

        if (!modal) return;

        modal.classList.add("show");

        document.body.style.overflow =
            "hidden";
    };

    const hideDemo = () => {

        if (!modal) return;

        modal.classList.remove("show");

        document.body.style.overflow =
            "";
    };

    demoButtons.forEach(button => {

        button.addEventListener(
            "click",
            openDemo
        );

    });

    if (closeModal) {

        closeModal.addEventListener(
            "click",
            hideDemo
        );

    }

    if (modal) {

        modal.addEventListener(
            "click",
            event => {

                if (
                    event.target === modal
                ) {
                    hideDemo();
                }

            }
        );

    }

    document.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Escape"
            ) {
                hideDemo();
            }

        }
    );


    /* =====================================================
       SEARCH
    ===================================================== */

    const searchButtons =
        document.querySelectorAll(
            ".search-button, [data-search]"
        );

    searchButtons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                const searchInput =
                    document.querySelector(
                        ".search-input"
                    );

                if (!searchInput) {

                    window.location.href =
                        "learn.html";

                    return;
                }

                const topic =
                    searchInput.value.trim();

                if (!topic) {

                    searchInput.focus();

                    return;
                }

                window.location.href =
                    "learn.html?topic=" +
                    encodeURIComponent(topic);

            }
        );

    });


    /* =====================================================
       SEARCH WITH ENTER
    ===================================================== */

    document
        .querySelectorAll(".search-input")
        .forEach(input => {

            input.addEventListener(
                "keydown",
                event => {

                    if (
                        event.key !== "Enter"
                    ) return;

                    const topic =
                        input.value.trim();

                    if (!topic) return;

                    window.location.href =
                        "learn.html?topic=" +
                        encodeURIComponent(topic);

                }
            );

        });


    /* =====================================================
       BUTTON PRESS EFFECT
    ===================================================== */

    document
        .querySelectorAll("button, .btn, .cta-button")
        .forEach(button => {

            button.addEventListener(
                "pointerdown",
                () => {

                    button.style.transform =
                        "scale(.97)";

                }
            );

            button.addEventListener(
                "pointerup",
                () => {

                    button.style.transform =
                        "";

                }
            );

            button.addEventListener(
                "pointerleave",
                () => {

                    button.style.transform =
                        "";

                }
            );

        });


    /* =====================================================
       PREVENT EMPTY LINKS
    ===================================================== */

    document
        .querySelectorAll('a[href="#"]')
        .forEach(link => {

            link.addEventListener(
                "click",
                event => {

                    event.preventDefault();

                }
            );

        });


    /* =====================================================
       ACTIVE PAGE NAVIGATION
    ===================================================== */

    const currentPage =
        window.location.pathname
            .split("/")
            .pop() || "index.html";

    document
        .querySelectorAll(".main-nav a")
        .forEach(link => {

            const href =
                link.getAttribute("href");

            if (!href) return;

            const page =
                href.split("#")[0];

            if (
                page === currentPage
            ) {

                link.classList.add(
                    "active"
                );

            }

        });


    /* =====================================================
       SIMPLE PAGE LOAD ANIMATION
    ===================================================== */

    document.body.classList.add(
        "page-loaded"
    );


    /* =====================================================
       VISUALIZE PAGE — QUICK OPEN
    ===================================================== */

    const visualizeButtons =
        document.querySelectorAll(
            '[data-visualize]'
        );

    visualizeButtons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                const topic =
                    button.dataset.visualize;

                if (!topic) {

                    window.location.href =
                        "visualize.html";

                    return;
                }

                window.location.href =
                    "visualize.html?topic=" +
                    encodeURIComponent(topic);

            }
        );

    });


    /* =====================================================
       QUIZ PAGE — QUICK OPEN
    ===================================================== */

    const quizButtons =
        document.querySelectorAll(
            '[data-quiz]'
        );

    quizButtons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                const topic =
                    button.dataset.quiz;

                if (!topic) {

                    window.location.href =
                        "quiz.html";

                    return;
                }

                window.location.href =
                    "quiz.html?topic=" +
                    encodeURIComponent(topic);

            }
        );

    });


    /* =====================================================
       KEYBOARD SHORTCUT
       Press "/" to focus search
    ===================================================== */

    document.addEventListener(
        "keydown",
        event => {

            if (
                event.key !== "/" ||
                event.ctrlKey ||
                event.metaKey ||
                event.altKey
            ) {
                return;
            }

            const active =
                document.activeElement;

            if (
                active &&
                (
                    active.tagName === "INPUT" ||
                    active.tagName === "TEXTAREA"
                )
            ) {
                return;
            }

            const search =
                document.querySelector(
                    ".search-input"
                );

            if (search) {

                event.preventDefault();

                search.focus();

            }

        }
    );


    /* =====================================================
       CONSOLE BRANDING
    ===================================================== */

    console.log(
        "%cJNAIVA",
        `
        font-size: 24px;
        font-weight: 700;
        letter-spacing: 3px;
        color: #111;
        `
    );

    console.log(
        "AI-powered visual learning platform."
    );

});