import { createRouter, createWebHistory } from "vue-router";

import mainRoutes from "./mainRoutes";
import authRoutes from "./authRoutes";
import restaurantRoutes from "./restaurantRoutes";
import foodRoutes from "./foodRoutes";

const routes = [
  ...mainRoutes,
  ...authRoutes,
  ...restaurantRoutes,
  ...foodRoutes,
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return new Promise((resolve) => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
      setTimeout(() => resolve({ left: 0, top: 0 }), 300);
    });
  },
});

export default router;
