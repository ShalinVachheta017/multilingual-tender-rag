(() => {
  const search = document.querySelector("#commit-search");
  const date = document.querySelector("#commit-date");
  const rows = Array.from(document.querySelectorAll("#commit-rows tr"));
  const count = document.querySelector("#result-count");
  const empty = document.querySelector("#empty-history");

  if (!search || !date || !count || !empty) return;

  const applyFilters = () => {
    const query = search.value.trim().toLocaleLowerCase();
    const selectedDate = date.value;
    let visible = 0;

    rows.forEach((row) => {
      const matchesQuery = !query || row.dataset.search.includes(query);
      const matchesDate = !selectedDate || row.dataset.date === selectedDate;
      const show = matchesQuery && matchesDate;
      row.hidden = !show;
      if (show) visible += 1;
    });

    count.textContent = `${visible} commit${visible === 1 ? "" : "s"}`;
    empty.hidden = visible !== 0;
  };

  search.addEventListener("input", applyFilters);
  date.addEventListener("change", applyFilters);
  applyFilters();
})();
