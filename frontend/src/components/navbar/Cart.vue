<template>
  <router-link to="/cart" class="relative inline-flex items-center group">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="h-6 w-6 text-gray-700 group-hover:text-black transition"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      stroke-width="2"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13l-1.5 7h13l-1.5-7M7 13h10"
      />
    </svg>
    <span
      v-if="cart.totalItems > 0"
      class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-semibold px-1.5 py-0.5 rounded-full shadow"
    >
      {{ cart.totalItems }}
    </span>
  </router-link>
</template>

<script setup>
import { useCart } from "../../composables/useCart";
const cart = useCart();
</script>
