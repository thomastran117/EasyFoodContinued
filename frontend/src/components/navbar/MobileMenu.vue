<template>
  <div class="sm:hidden" v-if="isOpen">
    <div>
      <button
        @click="mobileMoreOpen = !mobileMoreOpen"
        class="w-full flex justify-between items-center px-4 py-2 text-gray-700 hover:text-blue-600 focus:outline-none"
      >
        More
        <svg
          :class="{ 'transform rotate-180': mobileMoreOpen }"
          class="w-4 h-4 transition-transform duration-200"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      <div v-if="mobileMoreOpen" class="pl-4 space-y-1">
        <router-link
          to="/services"
          class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md"
          @click="
            isOpen = false;
            mobileMoreOpen = false;
          "
        >
          Services
        </router-link>
        <router-link
          to="/blog"
          class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md"
          @click="
            isOpen = false;
            mobileMoreOpen = false;
          "
        >
          Blog
        </router-link>
        <router-link
          to="/careers"
          class="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-md"
          @click="
            isOpen = false;
            mobileMoreOpen = false;
          "
        >
          Careers
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const isOpen = ref(false);
const dropdownOpen = ref(false);
const moreOpen = ref(false);
const mobileMoreOpen = ref(false);

const toggleMenu = () => (isOpen.value = !isOpen.value);
const toggleDropdown = () => (dropdownOpen.value = !dropdownOpen.value);
</script>
