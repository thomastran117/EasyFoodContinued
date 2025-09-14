import { defineStore } from "pinia";

export const useAuth = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("authToken") || null,
    email: localStorage.getItem("authEmail") || null,
  }),

  actions: {
    setAuth({ token, email }) {
      this.token = token;
      this.email = email;
      localStorage.setItem("authToken", token);
      localStorage.setItem("authEmail", email);
    },

    clearAuth() {
      this.token = null;
      this.email = null;
      localStorage.removeItem("authToken");
      localStorage.removeItem("authEmail");
    },
  },

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  persist: true,
});
