import { defineStore } from "pinia";

export const useAuth = defineStore("auth", {
  state: () => ({
    accessToken: null,

    email: localStorage.getItem("authEmail") || null,
    userType: localStorage.getItem("authUserType") || null,
    avatar: localStorage.getItem("authAvatar") || null,
    role: localStorage.getItem("authRole") || null,
  }),

  actions: {
    setAuth({ accessToken, email, userType, avatar, role }) {
      this.accessToken = accessToken;
      this.email = email;
      this.userType = userType;
      this.avatar = avatar;
      this.role = role;

      localStorage.setItem("authEmail", email);
      localStorage.setItem("authUserType", userType);
      localStorage.setItem("authAvatar", avatar);
      localStorage.setItem("authRole", role);
    },

    async clearAuth() {
      this.accessToken = null;
      this.email = null;
      this.userType = null;
      this.avatar = null;
      this.role = null;

      localStorage.removeItem("authEmail");
      localStorage.removeItem("authUserType");
      localStorage.removeItem("authAvatar");
      localStorage.removeItem("authRole");
    },
  },

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    getProfile: (state) => ({
      email: state.email,
      userType: state.userType,
      avatar: state.avatar,
      role: state.role,
    }),
  },
});
