import HomeView from "../views/main/HomeView.vue";
import AboutView from "../views/main/AboutView.vue";
import ContactView from "../views/main/ContactView.vue";
import CareerView from "../views/main/CareerView.vue";
import ServiceView from "../views/main/ServiceView.vue";
import TermsView from "../views/main/TermsView.vue";
import FAQsView from "../views/main/FAQsView.vue";
import HistoryView from "../views/main/HistoryView.vue";
import SurveyView from "../views/other/SurveyView.vue";
import ManageView from "../views/other/ManageView.vue";
import NotFoundView from "../views/error/NotFoundView.vue";

const LINK = import.meta.env.VITE_BACKEND_URL;

export default [
  { path: "/", name: "Home", component: HomeView },
  { path: "/about", name: "About", component: AboutView },
  { path: "/contact", name: "Contact", component: ContactView },
  { path: "/services", name: "Service", component: ServiceView },
  { path: "/careers", name: "Career", component: CareerView },
  {
    path: "/history",
    name: "History",
    component: HistoryView,
    props: () => ({ link: LINK }),
  },
  {
    path: "/survey",
    name: "Survey",
    component: SurveyView,
    props: () => ({ link: LINK }),
  },
  {
    path: "/manage",
    name: "Manage",
    component: ManageView,
  },
  { path: "/terms", name: "Terms and Conditions", component: TermsView },
  { path: "/faqs", name: "Frequently Asked Questions", component: FAQsView },
  { path: "/:pathMatch(.*)*", name: "Not Found", component: NotFoundView },
];
