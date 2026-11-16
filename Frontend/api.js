const API_BASE_URL = "http://127.0.0.1:8006";

function getToken() {
    return localStorage.getItem("access_token");
}

function requireLogin() {
    if (!getToken()) {
        window.location.href = "login.html";
    }
}

function logout() {
    localStorage.removeItem("access_token");
    window.location.href = "index.html";
}

async function apiRequest(path, options = {}) {
    const token = getToken();
    const headers = { ...(options.headers || {}) };

    if (token) headers.Authorization = `Bearer ${token}`;

    const isFormData = options.body instanceof FormData;
    if (!isFormData && options.body !== undefined) {
        headers["Content-Type"] = "application/json";
    }

    let response;
    try {
        response = await fetch(`${API_BASE_URL}${path}`, {
            ...options,
            headers
        });
    } catch (error) {
        throw new Error(
            `Cannot reach CareerAI backend at ${API_BASE_URL}. ` +
            `Check that FastAPI is running on port 8006.`
        );
    }

    if (response.status === 401) {
        localStorage.removeItem("access_token");
        window.location.href = "login.html";
        throw new Error("Your session expired. Please log in again.");
    }

    const contentType = response.headers.get("content-type") || "";
    const data = contentType.includes("application/json")
        ? await response.json()
        : await response.text();

    if (!response.ok) {
        const detail = data && data.detail ? data.detail : "Request failed.";
        throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
    }

    return data;
}

function jsonBody(value) {
    return JSON.stringify(value);
}

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, ch => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    })[ch]);
}

function attachLogout() {
    const button = document.getElementById("logoutButton");
    if (button) button.addEventListener("click", logout);
}

document.addEventListener("DOMContentLoaded", attachLogout);
