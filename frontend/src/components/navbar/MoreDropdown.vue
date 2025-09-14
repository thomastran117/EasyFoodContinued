<template>
  <div
    class="relative group"
    @mouseenter="open = true"
    @mouseleave="open = false"
  >
    <button
      class="inline-flex items-center space-x-1 text-gray-700 hover:text-blue-600 focus:outline-none"
      :aria-expanded="open.toString()"
    >
      <span>More</span>
      <svg
        class="h-4 w-4 transition-transform duration-300"
        :class="{ 'rotate-180': open }"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        stroke-width="2"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M19 9l-7 7-7-7"
        />
      </svg>
    </button>

    <transition name="fade-slide">
      <div
        v-if="open"
        class="absolute top-full mt-2 w-40 bg-white border border-gray-200 rounded-lg shadow-lg py-2 z-50"
      >
        <div
          class="absolute top-0 left-4 w-3 h-3 bg-white border-l border-t border-gray-200 transform rotate-45 -translate-y-1/2"
        ></div>
        <router-link
          v-for="link in dropdownLinks"
          :key="link.to"
          :to="link.to"
          class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md"
          @click="open = false"
        >
          {{ link.label }}
        </router-link>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from "vue";
const open = ref(false);
const dropdownLinks = [
  { label: "Services", to: "/services" },
  { label: "Contact", to: "/contact" },
];
</script>

<style>
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
.rotate-0 {
  transform: rotate(0deg);
}
.rotate-180 {
  transform: rotate(180deg);
}
</style>
