<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import Navbar from "./components/shared/Navbar.vue";
import Footer from "./components/shared/Footer.vue";
import Breadcrumb from "./components/shared/Breadcrumbs.vue";
import SessionManager from "./components/auth/SessionManager.vue";
const route = useRoute();

const breadcrumbs = computed(() => {
  const matched = route.matched.filter((r) => r.meta?.breadcrumb !== false);
  const crumbs = matched.map((r, index) => ({
    label: r.meta?.label || r.name,
    href: index < matched.length - 1 ? r.path : "",
  }));

  if (!crumbs.length || crumbs[0].label !== "Home") {
    crumbs.unshift({ label: "Home", href: "/" });
  }

  return crumbs;
});
</script>

<template>
  <SessionManager />
  <Navbar />
  <Breadcrumb :crumbs="breadcrumbs" />
  <router-view />
  <Footer />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
