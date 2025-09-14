<template>
  <div class="hidden sm:flex sm:flex-1 justify-center space-x-6 items-center">
    <router-link
      v-for="link in links"
      :key="link.to"
      :to="link.to"
      :class="[
        'text-gray-700 hover:text-blue-600 font-medium',
        route.path === link.to ? 'text-blue-600' : '',
      ]"
    >
      {{ link.label }}
    </router-link>

    <MoreDropdown />
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import MoreDropdown from "./MoreDropdown.vue";

const route = useRoute();
const links = [
  { label: "Home", to: "/" },
  { label: "About", to: "/about" },
  { label: "Browse", to: "/restaurant" },
];
</script>
