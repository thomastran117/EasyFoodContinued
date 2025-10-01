import FoodView from "../views/food/FoodView.vue";
import FoodManageView from "../views/food/FoodManageView.vue";
import FoodCreateView from "../views/food/FoodCreateView.vue";

const LINK = import.meta.env.VITE_BACKEND_URL;

export default [
  {
    path: "/manage/manage-food",
    name: "Manage Restaurant's Food",
    component: FoodManageView,
    props: () => ({ link: LINK }),
  },
  {
    path: "/manage/create-food",
    name: "Create Restaurant Food",
    component: FoodCreateView,
    props: () => ({ link: LINK }),
  },
];
