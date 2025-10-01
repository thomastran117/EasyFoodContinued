import AuthView from "../views/auth/AuthView.vue";
import PasswordView from "../views/auth/PasswordView.vue";
import VerifyEmailView from "../views/auth/VerifyEmailView.vue";
import ProfileManageView from "../views/profile/ProfileManageView.vue";
import MicrosoftCallbackView from "../views/auth/MicrosoftCallbackView.vue";
import GoogleCallbackView from "../views/auth/GoogleCallbackView.vue";

const LINK = import.meta.env.VITE_BACKEND_URL;

export default [
  {
    path: "/auth",
    name: "Auth",
    component: AuthView,
    props: () => ({ link: LINK }),
  },
  {
    path: "/auth/microsoft",
    name: "Microsoft",
    component: MicrosoftCallbackView,
  },
  {
    path: "/auth/google",
    name: "Google",
    component: GoogleCallbackView,
  },
  {
    path: "/verify-email",
    name: "Verify",
    component: VerifyEmailView,
    props: () => ({ link: LINK }),
  },
  {
    path: "/password",
    name: "Password",
    component: PasswordView,
    props: () => ({ link: LINK }),
  },
  {
    path: "/profile",
    name: "Profile",
    component: ProfileManageView,
    props: () => ({ link: LINK }),
  },
];
