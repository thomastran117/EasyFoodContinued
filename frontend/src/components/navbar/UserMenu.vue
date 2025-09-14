<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../../composables/useAuth";
import { useCart } from "../../composables/useCart";

import {
  UserIcon,
  ClockIcon,
  BuildingOffice2Icon,
  ArrowRightOnRectangleIcon,
} from "@heroicons/vue/24/outline";

const open = ref(false);
const isOpen = ref(false);

const auth = useAuth();
const cart = useCart();
const router = useRouter();

const isLoggedIn = computed(() => !!auth.token);
const firstInitial = computed(() =>
  auth.email ? auth.email.charAt(0).toUpperCase() : "?",
);

const logout = () => {
  auth.clearAuth();
  cart.clearCart();
  open.value = false;
  router.push("/");
};

const toggleMenu = () => (isOpen.value = !isOpen.value);
</script>

<template>
  <div class="flex items-center space-x-4 relative">
    <template v-if="isLoggedIn">
      <div
        class="relative"
        @mouseenter="open = true"
        @mouseleave="open = false"
      >
        <button
          class="flex items-center space-x-2 focus:outline-none"
          :aria-expanded="open.toString()"
        >
          <div
            class="w-10 h-10 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center hover:bg-blue-700"
          >
            {{ firstInitial }}
          </div>
          <svg
            class="h-4 w-4 text-blue-600 transition-transform duration-300"
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
            class="absolute right-0 mt-2 w-56 bg-white border border-gray-200 rounded-lg shadow-lg py-2 z-50"
          >
            <div
              class="absolute top-0 right-4 w-3 h-3 bg-white border-l border-t border-gray-200 transform rotate-45 -translate-y-1/2"
            ></div>

            <router-link
              to="/profile"
              class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md space-x-2"
            >
              <UserIcon class="w-5 h-5 text-gray-500" />
              <span>Profile</span>
            </router-link>

            <router-link
              to="/history"
              class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md space-x-2"
            >
              <ClockIcon class="w-5 h-5 text-gray-500" />
              <span>My Previous Actions</span>
            </router-link>

            <router-link
              to="/manage"
              class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md space-x-2"
            >
              <BuildingOffice2Icon class="w-5 h-5 text-gray-500" />
              <span>My Restaurant</span>
            </router-link>

            <button
              @click="logout"
              class="flex items-center w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md space-x-2"
            >
              <ArrowRightOnRectangleIcon class="w-5 h-5 text-gray-500" />
              <span>Logout</span>
            </button>
          </div>
        </transition>
      </div>
    </template>

    <router-link
      v-else
      to="/auth"
      class="hidden sm:inline-block px-4 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-md"
    >
      Login
    </router-link>

    <button
      @click="toggleMenu"
      class="sm:hidden text-gray-600 hover:text-blue-600 focus:outline-none"
      aria-label="Toggle menu"
    >
      <svg
        class="w-6 h-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          :d="isOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'"
        />
      </svg>
    </button>
  </div>
</template>
