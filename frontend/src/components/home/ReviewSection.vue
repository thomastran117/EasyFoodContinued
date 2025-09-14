<template>
  <section class="py-16 bg-white px-6 border-t border-gray-200">
    <div class="max-w-4xl mx-auto text-center mb-10">
      <h2 class="text-3xl font-bold text-gray-800">What People Are Saying</h2>
      <p class="text-gray-600 mt-4">
        Trusted by consumers and entreprenuers around the world.
      </p>
    </div>
    <div class="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
      <ReviewCard
        description="Absolutely love the simplicity and power of this setup. Perfect for expanding my audience."
        person="John D., Owner of YumChicken"
      />
      <ReviewCard
        description="Clean, simple, and gorgeous. This saved me loads of time when I want to order food."
        person="Bill S., Customer"
      />
    </div>
  </section>
</template>

<script setup>
import ReviewCard from "./ReviewCard.vue";
</script>
