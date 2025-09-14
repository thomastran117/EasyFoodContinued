<template>
  <div class="bg-gray-100 p-6 rounded-lg shadow-inner">
    <p class="italic text-gray-700 mb-4">“{{ description }}”</p>
    <div class="font-semibold text-blue-600">— {{ person }}</div>
  </div>
</template>

<script>
export default {
  props: {
    description: {
      type: String,
      required: true,
    },
    person: {
      type: String,
      required: true,
    },
  },
};
</script>
