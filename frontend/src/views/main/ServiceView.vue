<template>
  <main class="bg-gray-50 text-gray-800 font-sans">
    <!-- Hero Section -->
    <HeroCard
      title="Partner with EasyFood"
      subtitle="Grow your restaurant with our modern delivery and marketing platform."
      :showButtons="false"
    />

    <!-- Services Grid -->
    <section class="py-16 px-6 bg-gray-100">
      <div class="max-w-6xl mx-auto text-center mb-12">
        <h2 class="text-3xl font-bold">Services for Restaurants</h2>
        <p class="text-gray-600 mt-4">
          Tools to help you reach more customers, streamline operations, and
          increase revenue.
        </p>
      </div>
      <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        <div
          v-for="service in services"
          :key="service.title"
          class="bg-gray-50 p-6 rounded-xl shadow hover:shadow-md transition"
        >
          <div class="text-4xl text-blue-600 mb-4">{{ service.icon }}</div>
          <h3 class="text-xl font-semibold mb-2 text-blue-700">
            {{ service.title }}
          </h3>
          <p class="text-gray-600">{{ service.description }}</p>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="py-16 px-6 bg-white">
      <div class="max-w-5xl mx-auto text-center mb-12">
        <h2 class="text-3xl font-bold">How It Works</h2>
        <p class="text-gray-600 mt-4">
          Partnering with EasyFood is fast, easy, and profitable.
        </p>
      </div>
      <div class="grid md:grid-cols-3 gap-8 text-center">
        <div class="p-6">
          <div class="text-3xl mb-3 text-blue-600 font-bold">1</div>
          <h3 class="text-lg font-semibold mb-2">Sign Up</h3>
          <p class="text-gray-600">
            Register your restaurant and get listed on our platform within days.
          </p>
        </div>
        <div class="p-6">
          <div class="text-3xl mb-3 text-blue-600 font-bold">2</div>
          <h3 class="text-lg font-semibold mb-2">Receive Orders</h3>
          <p class="text-gray-600">
            Customers discover your menu, place orders, and choose delivery or
            pickup.
          </p>
        </div>
        <div class="p-6">
          <div class="text-3xl mb-3 text-blue-600 font-bold">3</div>
          <h3 class="text-lg font-semibold mb-2">Grow with Us</h3>
          <p class="text-gray-600">
            Track your performance and scale with our marketing and analytics
            tools.
          </p>
        </div>
      </div>
    </section>

    <!-- Why Choose Us -->
    <section class="py-16 px-6 bg-gray-100">
      <div class="max-w-5xl mx-auto text-center mb-12">
        <h2 class="text-3xl font-bold">Why Partner with EasyFood?</h2>
        <p class="text-gray-600 mt-4">
          We’re committed to helping your restaurant succeed — every step of the
          way.
        </p>
      </div>
      <div class="grid md:grid-cols-3 gap-8 text-left max-w-6xl mx-auto">
        <div class="bg-blue-50 p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-blue-700 mb-2">
            Expand Your Reach
          </h3>
          <p class="text-gray-600">
            Tap into thousands of hungry customers browsing EasyFood every day.
          </p>
        </div>
        <div class="bg-blue-50 p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-blue-700 mb-2">
            Seamless Logistics
          </h3>
          <p class="text-gray-600">
            From order to delivery, our platform makes everything easy and
            efficient.
          </p>
        </div>
        <div class="bg-blue-50 p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-blue-700 mb-2">
            Dedicated Support
          </h3>
          <p class="text-gray-600">
            Get real human support and insights tailored to your restaurant.
          </p>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 px-6 bg-blue-600 text-white text-center">
      <div class="max-w-3xl mx-auto">
        <h2 class="text-3xl font-bold mb-4">Join EasyFood Today</h2>
        <p class="text-lg mb-8">
          Start receiving more orders and growing your business with ease.
        </p>
        <router-link
          to="/auth"
          class="bg-white text-blue-600 font-semibold px-6 py-3 rounded-lg hover:bg-gray-100 transition"
        >
          Become a Partner
        </router-link>
      </div>
    </section>
  </main>
</template>

<script setup>
import HeroCard from "../../components/shared/HeroCard.vue";

const services = [
  {
    title: "Online Ordering",
    description:
      "Accept pickup and delivery orders from customers using our modern platform.",
    icon: "📱",
  },
  {
    title: "Marketing & Exposure",
    description:
      "Boost your visibility through featured listings, promos, and more.",
    icon: "📣",
  },
  {
    title: "Analytics Dashboard",
    description:
      "Track your orders, revenue, and customer feedback in real time.",
    icon: "📊",
  },
];
</script>

<style scoped></style>
