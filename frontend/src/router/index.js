import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/main/HomeView.vue";
import AboutView from "../views/main/AboutView.vue";
import ContactView from "../views/main/ContactView.vue";
import AuthView from "../views/auth/AuthView.vue";
import PasswordView from "../views/auth/PasswordView.vue";
import CareerView from "../views/main/CareerView.vue";
import ServiceView from "../views/main/ServiceView.vue";
import TermsView from "../views/main/TermsView.vue";
import FAQsView from "../views/main/FAQsView.vue";
import VerifyEmailView from "../views/auth/VerifyEmailView.vue";
import RestaurantView from "../views/restaurant/RestaurantView.vue";
import CartView from "../views/order/CartView.vue";
import RestaurantManageView from "../views/restaurant/RestaurantManageView.vue";
import RestaurantCreateView from "../views/restaurant/RestaurantCreateView.vue";
import RestaurantUpdateView from "../views/restaurant/RestaurantUpdateView.vue";
import ProfileManageView from "../views/profile/ProfileManageView.vue";
import SurveyView from "../views/other/SurveyView.vue";
import FoodView from "../views/food/FoodView.vue";
import FoodManageView from "../views/food/FoodManageView.vue";
import FoodCreateView from "../views/food/FoodCreateView.vue";
import ManageView from "../views/other/ManageView.vue";
import RestaurantIndex from "../views/restaurant/RestaurantIndex.vue";
import OrderView from "../views/order/OrderView.vue";
import OrderRestaurantView from "../views/order/OrderRestaurantView.vue";
import ReviewView from "../views/review/ReviewView.vue";
import NotFoundView from "../views/error/NotFoundView.vue";
import HistoryView from "../views/main/HistoryView.vue";
import OrderConfirmationView from "../views/order/OrderConfirmationView.vue";

const LINK = import.meta.env.VITE_BACKEND_URL;

const routes = [
  { path: "/", name: "Home", component: HomeView },
  { path: "/about", name: "About", component: AboutView },
  { path: "/contact", name: "Contact", component: ContactView },
  { path: "/services", name: "Service", component: ServiceView },
  { path: "/careers", name: "Career", component: CareerView },
  {
    path: "/history",
    name: "History",
    component: HistoryView,
    props: (route) => ({ link: LINK }),
  },
  {
    path: "/auth",
    name: "Auth",
    component: AuthView,
    props: (route) => ({ link: LINK }),
  },
  { path: "/terms", name: "Terms and Conditions", component: TermsView },
  { path: "/faqs", name: "Frequently Asked Questions", component: FAQsView },
  {
    path: "/verify-email",
    name: "Verify",
    component: VerifyEmailView,
    props: (route) => ({ link: LINK }),
  },
  {
    path: "/password",
    name: "Password",
    component: PasswordView,
    props: (route) => ({ link: LINK }),
  },
  { path: "/profile", name: "Profile", component: ProfileManageView, props: (route) => ({ link: LINK }), },
  {
    path: "/cart",
    name: "Cart",
    component: CartView,
    props: (route) => ({ link: LINK }),
  },
  {
    path: "/survey",
    name: "Survey",
    component: SurveyView,
    props: (route) => ({ link: LINK }),
  },
  {
    path: "/manage",
    name: "Manage",
    component: ManageView,
    children: [
      {
        path: "create",
        name: "Create Restaurant",
        component: RestaurantCreateView,
        props: (route) => ({ link: LINK }),
      },
      {
        path: "",
        name: "My Restaurant",
        component: RestaurantManageView,
        props: (route) => ({ link: LINK }),
      },
      {
        path: "update/:id?",
        name: "Update Restaurant",
        component: RestaurantUpdateView,
        props: true,
        props: (route) => ({ link: LINK }),
      },
      {
        path: "manage-food",
        name: "Manage Restaurant's Food",
        component: FoodManageView,
        props: (route) => ({ link: LINK }),
      },
      {
        path: "create-food",
        name: "Create Restaurant Food",
        component: FoodCreateView,
        props: (route) => ({ link: LINK }),
      },
      {
        path: "manage-review",
        name: "Manage Review",
        component: ReviewView,
      },
    ],
  },
  {
    path: "/restaurant",
    name: "Restaurant",
    component: RestaurantIndex,
    children: [
      {
        path: "",
        component: RestaurantView,
        props: (route) => ({ link: LINK }),
      },
      {
        path: ":id",
        name: "Restaurant Details",
        component: FoodView,
        props: (route) => ({ link: LINK }),
      },
    ],
  },
  {
    path: "/order",
    name: "Order",
    component: OrderView,
    children: [
      {
        path: "restaurant",
        name: "Order Restaurant",
        component: OrderRestaurantView,
      },
      {
        path: "confirmation",
        name: "Order Confirmation",
        component: OrderConfirmationView,
      },
    ],
  },
  { path: "/:pathMatch(.*)*", name: "Not Found", component: NotFoundView },
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
