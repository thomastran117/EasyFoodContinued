<template>
  <div class="bg-blue-50 p-5 rounded-xl shadow">
    <h3 class="text-xl font-semibold mb-2 text-blue-700">{{ title }}</h3>
    <p>{{ subtitle }}</p>
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
  },
};
</script>
