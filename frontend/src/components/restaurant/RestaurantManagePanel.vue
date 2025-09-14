<template>
  <div
    class="bg-white bg-opacity-30 backdrop-blur-md rounded-xl shadow-lg mt-6 p-6 border border-blue-200"
  >
    <h3 class="text-xl font-semibold mb-5 text-blue-900">Manage Restaurant</h3>
    <div class="flex flex-wrap gap-4">
      <router-link
        :to="`/manage/update/${restaurantId}`"
        class="px-5 py-2 rounded-md bg-blue-500 text-white hover:bg-blue-600 transition duration-300 shadow-sm"
      >
        ✏️ Update
      </router-link>
      <button
        @click="$emit('delete')"
        class="px-5 py-2 rounded-md bg-blue-500 text-white hover:bg-blue-600 transition duration-300 shadow-sm"
      >
        🗑️ Delete
      </button>
      <router-link
        :to="`/manage/manage-food/`"
        class="px-5 py-2 rounded-md bg-blue-500 text-white hover:bg-blue-600 transition duration-300 shadow-sm"
      >
        View Foods
      </router-link>
      <router-link
        :to="`/manage/manage-review/`"
        class="px-5 py-2 rounded-md bg-blue-500 text-white hover:bg-blue-600 transition duration-300 shadow-sm"
      >
        View Reviews
      </router-link>
    </div>
  </div>
</template>

<script setup>
defineProps({ restaurantId: Number });
</script>
