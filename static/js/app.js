document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      const open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open);
    });
  }
  document.querySelectorAll(".bar[data-height]").forEach(function (bar, index) {
    window.setTimeout(function () { bar.style.setProperty("--bar-height", bar.dataset.height + "%"); }, 100 + index * 80);
  });
});
