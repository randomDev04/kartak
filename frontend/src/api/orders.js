import { request } from "./client";

export const orders = {
  listOrders: () => request("/orders", { auth: true }),
  createOrder: (items) => request("/orders", { method: "POST", body: { items }, auth: true }),
};
