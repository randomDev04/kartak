const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function getToken() {
  return localStorage.getItem("token");
}

export async function request(path, { method = "GET", body, auth = false, form = false } = {}) {
  const headers = {};
  if (body && !form) headers["Content-Type"] = "application/json";
  if (auth) headers["Authorization"] = `Bearer ${getToken()}`;

  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      method,
      headers,
      body: form ? body : body ? JSON.stringify(body) : undefined,
    });

    if (res.status === 401) {
      window.dispatchEvent(new Event("unauthorized"));
      throw new Error("Unauthorized");
    }

    if (!res.ok) {
      const detail = await res.json().catch(() => ({}));
      throw new Error(detail.detail || `Request failed with ${res.status}`);
    }
    if (res.status === 204) return null;
    return await res.json();
  } catch (err) {
    if (err.name === "TypeError") {
      throw new Error("Unable to connect to the server. Please check your connection.");
    }
    throw err;
  }
}
