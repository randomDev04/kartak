import { request } from "./api/client";

export const api = {
  register: (email, password) => request("/auth/register", { method: "POST", body: { email, password } }),

  login: (email, password) => {
    const form = new URLSearchParams();
    form.set("username", email);
    form.set("password", password);
    return request("/auth/login", { method: "POST", body: form, form: true });
  },

  listProducts: () => request("/products"),

  createProduct: (product) => request("/products", { method: "POST", body: product, auth: true }),

  listOrders: () => request("/orders", { auth: true }),

  createOrder: (items) => request("/orders", { method: "POST", body: { items }, auth: true }),
};
