import { auth } from "./auth";
import { products } from "./products";
import { orders } from "./orders";

export const api = {
  ...auth,
  ...products,
  ...orders,
};
