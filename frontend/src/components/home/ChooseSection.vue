<template>
  <section class="py-16 px-6 bg-gray-100">
    <div class="max-w-6xl mx-auto text-center mb-12">
      <h2 class="text-3xl font-bold text-gray-800">Why Order with EasyFood?</h2>
      <p class="text-gray-600 mt-4">
        We deliver great food, fast service, and a seamless experience every
        time.
      </p>
    </div>
    <div class="grid md:grid-cols-3 gap-8 text-left max-w-6xl mx-auto">
      <ChooseCard
        title="Fast & Reliable"
        subtitle="Get your favorite meals delivered quickly and fresh, every time."
        icon="⚡"
      />
      <ChooseCard
        title="Diverse Choices"
        subtitle="From local favorites to trending dishes, find exactly what you crave."
        icon="🍽️"
      />
      <ChooseCard
        title="Customer First"
        subtitle="24/7 support and easy refunds — your satisfaction is our priority."
        icon="🤝"
      />
    </div>
  </section>
</template>

<script setup>
import ChooseCard from "./ChooseCard.vue";
</script>
