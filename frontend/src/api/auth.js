import { request } from "./client";

export const auth = {
  register: (email, password) => request("/auth/register", { method: "POST", body: { email, password } }),

  login: (email, password) => {
    const form = new URLSearchParams();
    form.set("username", email);
    form.set("password", password);
    return request("/auth/login", { method: "POST", body: form, form: true });
  },
};
