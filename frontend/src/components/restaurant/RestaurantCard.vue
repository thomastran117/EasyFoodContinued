<template>
  <div
    class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition flex flex-col"
  >
    <img
      :src="
        restaurant.logoUrl ||
        'https://via.placeholder.com/400x200?text=No+Image'
      "
      alt="Restaurant Logo"
      class="w-full h-48 object-cover rounded-t-lg"
    />
    <div class="p-5 flex-1 flex flex-col justify-between space-y-4">
      <div>
        <h2 class="text-xl font-bold text-gray-800">
          {{ restaurant.name }}
        </h2>
        <div v-html="restaurant.description"></div>
        <p class="text-sm text-blue-600 font-medium">
          📍 {{ restaurant.location }}
        </p>
      </div>
      <router-link
        :to="`/restaurant/${restaurant.id}`"
        class="inline-block mt-4 text-center bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
      >
        View Restaurant
      </router-link>
    </div>
  </div>
</template>

<script setup>
defineProps({
  restaurant: {
    type: Object,
    required: true,
  },
});
</script>
