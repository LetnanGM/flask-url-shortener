class shortener {
  constructor() {
    this.target_url = document.getElementById("urlInput");
  }

  async send_url() {
    const inputed = this.target_url.value.trim();
    if (!inputed) {
      inputed.classList.add("is-invalid");
      setTimeout(() => {
        inputed.classList.remove("is-invalid");
      }, 1500);
      return;
    }

    const response = await fetch("/api/v1/shorturl.php", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: inputed,
      }),
    });

    if (response.status == 404) {
      alert("Service maybe down or Unavailable right now.")
    }

    const respjson = await response.json();
    const box = document.getElementById("resultBox");
    const link = document.getElementById("resultLink");
    link.textContent = `https://${document.domain}/${respjson.shorten_id}`;
    link.href = respjson.redirect;

    box.classList.add("show");
    box.classList.add("animate__animated", "animate__fadeIn");
  }
}

function copyLink() {
  const link = document.getElementById("resultLink").textContent;
  navigator.clipboard.writeText(link).then(() => {
    const btn = document.querySelector(".btn-copy");
    btn.innerHTML = '<i class="bi bi-check-lg me-1"></i>Copied!';
    setTimeout(
      () => (btn.innerHTML = '<i class="bi bi-clipboard me-1"></i>Copy'),
      2000
    );
  });
}

function goRedirect(url) {
  window.location.href = url;
}

function shortthis() {
  const shorten = new shortener();
  shorten.send_url();
}

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("urlInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const shorten = new shortener();
      shorten.send_url();
    }
  });
});
