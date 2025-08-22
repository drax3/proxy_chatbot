// --- auth helpers ---
function getToken() {
  return localStorage.getItem("access_token");
}
function setToken(t) {
  localStorage.setItem("access_token", t);
}
function clearToken() {
  localStorage.removeItem("access_token");
}
function authHeaders() {
  const t = getToken();
  return t ? { Authorization: "Bearer " + t } : {};
}
function requireAuthOrRedirect() {
  if (!getToken()) window.location.href = "/";
}
function redirectToLogin() {
  clearToken();
  window.location.href = "/";
}

// --- logout ---
const logoutBtn = document.getElementById("logoutBtn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    clearToken();
    window.location.href = "/";
  });
}

// --- small util ---
function escapeHtml(str) {
  return (str || "").replace(/[&<>"']/g, s => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[s]));
}
