<template>
  <section class="py-16 px-6 bg-gray-100">
    <div class="max-w-6xl mx-auto text-center mb-12">
      <h2 class="text-3xl font-bold text-gray-800">
        Why Customers Love EasyFood
      </h2>
      <p class="text-gray-600 mt-4">
        We make ordering food simple, fast, and enjoyable — every time.
      </p>
    </div>
    <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
      <FeatureCard
        title="Fast & Reliable Delivery"
        subtitle="Your favorite meals delivered hot and on time, every time."
        icon="🚚"
      />
      <FeatureCard
        title="Browse Local Favorites"
        subtitle="Discover top-rated restaurants and hidden gems near you."
        icon="🍔"
      />
      <FeatureCard
        title="Easy & Secure Payments"
        subtitle="Pay your way — with credit, debit, or digital wallets."
        icon="💳"
      />
    </div>
  </section>
</template>

<script setup>
import FeatureCard from "./FeatureCard.vue";
</script>
