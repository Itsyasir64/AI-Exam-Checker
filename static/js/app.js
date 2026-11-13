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
  const search = document.querySelector("#exam-search");
  const rows = document.querySelectorAll(".exam-row");
  const empty = document.querySelector("#no-exam-match");
  if (search && rows.length) {
    search.addEventListener("input", function () {
      const query = search.value.trim().toLowerCase();
      let visible = 0;
      rows.forEach(function (row) {
        const matches = !query || row.dataset.search.includes(query);
        row.classList.toggle("is-hidden", !matches);
        if (matches) visible += 1;
      });
      if (empty) empty.hidden = visible !== 0;
    });
  }
});
