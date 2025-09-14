<template>
  <div class="bg-white rounded-xl shadow p-6 flex flex-col items-center">
    <img
      :src="restaurant.logoUrl"
      class="w-28 h-28 object-cover rounded-full mb-4"
    />
    <h2 class="text-xl font-semibold">{{ restaurant.name }}</h2>
    <div v-html="restaurant.description"></div>
    <p class="text-sm text-gray-500 mt-1">{{ restaurant.location }}</p>
    <router-link
      :to="`/restaurant/${restaurant.id}`"
      class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
    >
      View Restaurant
    </router-link>
  </div>
</template>

<script setup>
defineProps({ restaurant: Object });
</script>
