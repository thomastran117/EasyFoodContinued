<template>
  <div class="flex justify-center items-center flex-col py-20 text-gray-500">
    <svg
      class="animate-spin h-10 w-10 text-blue-600 mb-4"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      />
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
      />
    </svg>
    <p class="text-lg font-medium">Fetching {{ resource }}...</p>
  </div>
</template>

<script setup>
defineProps({
  resource: {
    type: String,
    default: "data",
  },
});
</script>
