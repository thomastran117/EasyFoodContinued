<template>
  <section class="bg-white py-20 px-6 text-center shadow-sm">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-5xl font-extrabold text-blue-600 mb-6">
        {{ title }}
      </h1>
      <p class="text-xl text-gray-600 mb-8">
        {{ subtitle }}
      </p>
      <div v-if="showButtons" class="flex justify-center gap-4 flex-wrap">
        <router-link
          to="/restaurant"
          class="bg-blue-600 text-white px-6 py-3 rounded-lg shadow hover:bg-blue-700 transition"
        >
          Get Started
        </router-link>
        <router-link
          to="/services"
          class="border border-blue-600 text-blue-600 px-6 py-3 rounded-lg hover:bg-blue-50 transition"
        >
          Learn More
        </router-link>
      </div>
    </div>
  </section>
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
    showButtons: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
