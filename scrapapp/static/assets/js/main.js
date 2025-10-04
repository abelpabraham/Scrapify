// main.js
document.addEventListener("DOMContentLoaded", () => {
  // year in footer
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // toast helper
  window.showToast = function (
    title = "Notice",
    body = "Action completed",
    autohide = 3000
  ) {
    const container = document.querySelector(".toast-container");
    const toastEl = document.createElement("div");
    toastEl.className =
      "toast align-items-center text-bg-white border-0 p-3 toast-custom";
    toastEl.role = "alert";
    toastEl.ariaLive = "assertive";
    toastEl.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">
          <strong>${title}</strong><div class="small text-muted">${body}</div>
        </div>
        <button type="button" class="btn-close btn-close-black ms-2 m-auto" data-bs-dismiss="toast"></button>
      </div>`;
    container.appendChild(toastEl);
    const bsToast = new bootstrap.Toast(toastEl, { delay: autohide });
    bsToast.show();
    toastEl.addEventListener("hidden.bs.toast", () => toastEl.remove());
  };

  // Demo call
  // showToast('Welcome', 'You are now viewing GreenCycle.');

  // Initialize Charts (if elements exist)
  if (document.getElementById("analyticsChart")) {
    const ctx = document.getElementById("analyticsChart").getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: ["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
        datasets: [
          {
            label: "Recycled (kg)",
            data: [3200, 4100, 4700, 5200, 6100, 5400, 5800],
            borderWidth: 2,
            tension: 0.3,
            borderColor: "#40B97A",
            backgroundColor: "rgba(64,185,122,0.08)",
            fill: true,
            pointRadius: 4,
          },
        ],
      },
      options: {
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: "rgba(9,29,20,0.04)" } },
        },
      },
    });
  }

  // Initialize a small map (Leaflet)
  if (document.getElementById("map")) {
    const map = L.map("map", { scrollWheelZoom: false }).setView(
      [28.6139, 77.209],
      12
    );
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);
    // demo markers
    L.marker([28.6353, 77.2247]).addTo(map).bindPopup("Dealer A").openPopup();
    L.marker([28.6016, 77.23]).addTo(map).bindPopup("User pickup location");
  }

  // Auth toggle (in auth.html uses #auth-toggle)
  const authToggle = document.getElementById("auth-toggle");
  if (authToggle) {
    authToggle.addEventListener("click", (e) => {
      const panel = document.querySelector(".auth-form-panel");
      panel.classList.toggle("show-register");
      // add aria
      const isReg = panel.classList.contains("show-register");
      authToggle.setAttribute("aria-pressed", isReg ? "true" : "false");
    });
  }

  // Microinteraction: buttons lift
  document.querySelectorAll("button, .btn").forEach((btn) => {
    btn.addEventListener(
      "mouseenter",
      () => (btn.style.transform = "translateY(-3px)")
    );
    btn.addEventListener(
      "mouseleave",
      () => (btn.style.transform = "translateY(0)")
    );
  });
});

document.addEventListener("scroll", function () {
  const nav = document.querySelector(".topbar-navbar");
  if (window.scrollY > 16) nav.classList.add("scrolled");
  else nav.classList.remove("scrolled");
});
