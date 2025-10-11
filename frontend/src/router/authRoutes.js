import AuthView from "../views/auth/AuthView.vue";
import ForgotPasswordView from "../views/auth/ForgotPasswordView.vue";
import ChangePasswordView from "../views/auth/ChangePasswordView.vue";
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
    path: "/auth/verify",
    name: "Verify",
    component: VerifyEmailView,
    props: () => ({ link: LINK }),
  },
  {
    path: "/auth/forgot-password",
    name: "Forgot Password",
    component: ForgotPasswordView,
    props: () => ({ link: LINK }),
  },
  {
    path: "/profile",
    name: "Profile",
    component: ProfileManageView,
    props: () => ({ link: LINK }),
  },
];
