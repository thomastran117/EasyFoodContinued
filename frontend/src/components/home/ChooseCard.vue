<template>
  <div class="bg-white p-6 rounded-lg shadow">
    <div class="text-blue-600 text-3xl mb-3">{{ icon }}</div>
    <h3 class="text-lg font-semibold">{{ title }}</h3>
    <p class="text-gray-600">
      {{ subtitle }}
    </p>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      required: true,
    },
  },
};
</script>
