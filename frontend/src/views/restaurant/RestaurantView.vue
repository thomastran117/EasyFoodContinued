<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import LoadingState from "../../components/shared/LoadingState.vue";
import ErrorState from "../../components/shared/ErrorState.vue";
import RestaurantList from "../../components/restaurant/RestaurantList.vue";
import HeroCard from "../../components/shared/HeroCard.vue";

const props = defineProps({ link: String });
const restaurants = ref([]);
const loading = ref(true);
const error = ref(false);
const errorMessage = ref("");

const title = ref("");
const description = ref("");
const location = ref("");

const fetchRestaurants = async () => {
  loading.value = true;
  error.value = false;
  errorMessage.value = "";

  try {
    const response = await axios.get(`${props.link}/api/restaurant/`, {
      params: {
        title: title.value || undefined,
        description: description.value || undefined,
        location: location.value || undefined,
      },
    });

    restaurants.value = response.data.restaurants || [];
  } catch (err) {
    error.value = true;
    errorMessage.value = err?.response?.status
      ? `Error ${err.response.status}: ${err.response.statusText}`
      : "Network error or server unavailable.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchRestaurants();
});
</script>

<template>
  <HeroCard
    title="Browse Restaurants"
    subtitle="Search for restaurants and menus"
    :showButtons="false"
  />

  <section
    class="bg-yellow-100 border-l-4 border-yellow-400 text-yellow-800 p-6 my-4 max-w-6xl mx-auto rounded-xl shadow-md flex items-center justify-between flex-wrap gap-4"
  >
    <div>
      <h2 class="text-xl font-semibold">
        🎉 Get 30% Off Your First Few Orders!
      </h2>
      <p class="text-sm mt-1">
        Enjoy a limited-time discount on your first purchases from participating
        restaurants.
      </p>
    </div>
    <router-link
      to="/"
      class="bg-yellow-400 hover:bg-yellow-500 text-white px-5 py-2 rounded-md font-semibold transition"
    >
      Browse Deals
    </router-link>
  </section>
  <main class="min-h-screen bg-gray-50 text-gray-800 font-sans py-12 px-6">
    <section class="max-w-6xl mx-auto">

<form
  @submit.prevent="fetchRestaurants"
  class="mb-10 bg-white p-6 rounded-2xl shadow-lg grid grid-cols-1 md:grid-cols-3 gap-6 items-end border border-gray-200"
>
  <div>
    <label
      class="block text-sm font-semibold text-gray-800 mb-1 flex items-center gap-1"
    >
      <svg
        class="h-4 w-4 text-green-500"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M5 13l4 4L19 7"
        />
      </svg>
      Title
    </label>
    <input
      v-model="title"
      type="text"
      placeholder="e.g. Pizza Palace"
      class="modern-input"
    />
  </div>

  <div>
    <label
      class="block text-sm font-semibold text-gray-800 mb-1 flex items-center gap-1"
    >
      <svg
        class="h-4 w-4 text-green-500"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M5 13l4 4L19 7"
        />
      </svg>
      Description
    </label>
    <input
      v-model="description"
      type="text"
      placeholder="e.g. Italian cuisine"
      class="modern-input"
    />
  </div>

  <div>
    <label
      class="block text-sm font-semibold text-gray-800 mb-1 flex items-center gap-1"
    >
      <svg
        class="h-4 w-4 text-green-500"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M5 13l4 4L19 7"
        />
      </svg>
      Location
    </label>
    <input
      v-model="location"
      type="text"
      placeholder="e.g. Toronto"
      class="modern-input"
    />
  </div>

  <div class="md:col-span-3 flex justify-end mt-2">
    <button
      type="submit"
      class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-xl shadow-sm transition-all duration-200"
    >
      🔍 Search
    </button>
  </div>
</form>


      <LoadingState v-if="loading" resource="restaurants" />
      <ErrorState
        v-else-if="error"
        resource="restaurants"
        :message="errorMessage"
        :on-retry="fetchRestaurants"
      />

      <div
        v-else-if="restaurants.length === 0"
        class="text-center text-gray-600 py-10"
      >
        <p class="text-lg font-medium">No restaurants found.</p>
      </div>

      <RestaurantList v-else :restaurants="restaurants" />
    </section>
  </main>
</template>

<style scoped>
  .modern-input {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 2px solid #d1d5db;
    border-radius: 0.75rem;
    background-color: #f9fafb;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    font-size: 1rem;
    outline-offset: 2px;
  }

  .modern-input:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.4);
    background-color: white;
  }
</style>