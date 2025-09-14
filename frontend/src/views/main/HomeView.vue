<template>
  <main class="min-h-screen bg-gray-50 text-gray-800 font-sans">
    <HeroCard
      title="EasyFood — Delicious Meals, Delivered Fast"
      subtitle="Order from local favorites and explore new tastes, all at your fingertips."
      :showButtons="true"
    />

    <FeatureSection />
    <DiscoverSection />
    <ChooseSection />
    <ReviewSection />
    <CTASection />
  </main>
</template>

<script setup>
import HeroCard from "../../components/shared/HeroCard.vue";
import FeatureSection from "../../components/home/FeatureSection.vue";
import ReviewSection from "../../components/home/ReviewSection.vue";
import DiscoverSection from "../../components/home/DiscoverSection.vue";
import ChooseSection from "../../components/home/ChooseSection.vue";
import CTASection from "../../components/home/CTASection.vue";
</script>

<style scoped></style>
