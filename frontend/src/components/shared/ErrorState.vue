<template>
  <div
    class="bg-red-50 border border-red-200 p-6 rounded-lg shadow text-center max-w-xl mx-auto"
  >
    <h2 class="text-2xl font-semibold text-red-600 mb-2">
      Oops! Something went wrong.
    </h2>
    <p class="text-gray-700">We couldn't load {{ resource }} at the moment.</p>
    <p v-if="message" class="text-sm text-red-500 italic mt-2">
      ({{ message }})
    </p>

    <button
      v-if="onRetry"
      @click="onRetry"
      class="mt-4 inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
    >
      Retry
    </button>
  </div>
</template>

<script setup>
defineProps({
  resource: {
    type: String,
    default: "the requested content",
  },
  message: {
    type: String,
    default: "",
  },
  onRetry: {
    type: Function,
    default: null,
  },
});
</script>
