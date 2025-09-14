<template>
  <section class="py-16 px-6 bg-white">
    <div class="max-w-5xl mx-auto text-center">
      <h2 class="text-3xl font-bold text-gray-800">
        Discover More with EasyFood
      </h2>
      <p class="text-gray-600 mt-4 mb-12">
        Explore exclusive deals, new restaurants, and features to enhance your
        food ordering experience.
      </p>
      <div class="grid sm:grid-cols-2 md:grid-cols-3 gap-6">
        <DiscoverCard
          title="Exclusive Discounts"
          subtitle="Enjoy special offers and 30% off on your first few orders."
        />
        <DiscoverCard
          title="Real-time Order Tracking"
          subtitle="Watch your food as it’s prepared and delivered, step by step."
        />
        <DiscoverCard
          title="Personalized Recommendations"
          subtitle="Get meal suggestions tailored to your taste and past orders."
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import DiscoverCard from "./DiscoverCard.vue";
</script>
