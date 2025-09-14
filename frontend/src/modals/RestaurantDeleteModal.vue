<template>
  <div
    class="fixed inset-0 bg-opacity-60 backdrop-blur-sm flex items-center justify-center z-50"
  >
    <div
      class="bg-white rounded-lg p-6 max-w-sm w-full shadow-xl border border-gray-300"
    >
      <h3 class="text-lg font-semibold mb-2 text-red-600">Confirm Deletion</h3>
      <p class="text-sm text-gray-700 mb-4">
        Are you sure you want to delete <strong>{{ restaurant.name }}</strong
        >? This cannot be undone.
      </p>
      <div class="flex justify-end gap-2">
        <button
          @click="$emit('cancel')"
          class="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
        >
          Cancel
        </button>
        <button
          @click="$emit('confirm')"
          class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ restaurant: Object });
defineEmits(["cancel", "confirm"]);
</script>
