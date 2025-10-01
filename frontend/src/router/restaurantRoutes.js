import RestaurantIndex from "../views/restaurant/RestaurantIndex.vue";
import RestaurantView from "../views/restaurant/RestaurantView.vue";
import RestaurantManageView from "../views/restaurant/RestaurantManageView.vue";
import RestaurantCreateView from "../views/restaurant/RestaurantCreateView.vue";
import RestaurantUpdateView from "../views/restaurant/RestaurantUpdateView.vue";
import ReviewView from "../views/review/ReviewView.vue";

const LINK = import.meta.env.VITE_BACKEND_URL;

export default [
  {
    path: "/restaurant",
    name: "Restaurant",
    component: RestaurantIndex,
    children: [
      {
        path: "",
        component: RestaurantView,
        props: () => ({ link: LINK }),
      },
      {
        path: ":id",
        name: "Restaurant Details",
        component: () => import("../views/food/FoodView.vue"),
        props: () => ({ link: LINK }),
      },
    ],
  },
  {
    path: "/manage",
    name: "Manage Restaurant",
    component: RestaurantManageView,
    props: () => ({ link: LINK }),
    children: [
      {
        path: "create",
        name: "Create Restaurant",
        component: RestaurantCreateView,
        props: () => ({ link: LINK }),
      },
      {
        path: "update/:id?",
        name: "Update Restaurant",
        component: RestaurantUpdateView,
        props: true,
      },
      {
        path: "manage-review",
        name: "Manage Review",
        component: ReviewView,
      },
    ],
  },
];
