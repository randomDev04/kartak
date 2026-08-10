import { request } from "./client";

export const products = {
  listProducts: () => request("/products"),
  createProduct: (product) => request("/products", { method: "POST", body: product, auth: true }),
};
