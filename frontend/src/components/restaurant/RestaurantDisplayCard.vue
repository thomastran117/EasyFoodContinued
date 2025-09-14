<template>
  <div
    class="bg-white border border-gray-200 rounded-2xl shadow-md transition flex flex-col lg:flex-row overflow-hidden"
  >
    <img
      :src="
        restaurant.logoUrl ||
        'https://via.placeholder.com/600x400?text=No+Image'
      "
      alt="Restaurant Logo"
      class="w-full h-64 lg:w-1/2 lg:h-auto object-cover"
    />

    <div class="p-8 flex-1 flex flex-col justify-center space-y-4">
      <h2 class="text-3xl font-extrabold text-blue-700">
        {{ restaurant.name }}
      </h2>

      <div
        class="text-gray-700 text-base leading-relaxed"
        v-html="restaurant.description"
      />

      <p class="text-lg text-blue-600 font-semibold flex items-center">
        📍 <span class="ml-1">{{ restaurant.location }}</span>
      </p>
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
