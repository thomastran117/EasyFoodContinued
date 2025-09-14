<template>
  <main class="bg-gray-50 text-gray-800 font-sans">
    <!-- Hero Section -->
    <HeroCard
      title="Join our Team"
      subtitle="We're building a product that empowers restaurants globally."
      :showButtons="false"
    />

    <!-- Open Positions -->
    <section class="py-16 px-6">
      <div class="max-w-6xl mx-auto mb-12 text-center">
        <h2 class="text-3xl font-bold">Open Roles</h2>
        <p class="text-gray-600 mt-4">
          We’re always on the lookout for talented people. Find your fit below.
        </p>
      </div>
      <div class="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
        <div
          v-for="role in roles"
          :key="role.title"
          class="bg-white p-6 rounded-xl shadow hover:shadow-md transition"
        >
          <component :is="role.icon" class="w-8 h-8 text-blue-600 mb-4" />
          <h3 class="text-xl font-semibold text-blue-700 mb-2">
            {{ role.title }}
          </h3>
          <p class="text-gray-600 mb-4">{{ role.description }}</p>
          <div class="text-sm text-gray-500 mb-4">
            {{ role.location }} • {{ role.type }}
          </div>
          <router-link
            to="/apply"
            class="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
          >
            Apply Now
          </router-link>
        </div>
      </div>
    </section>

    <!-- Perks & Benefits -->
    <section class="py-16 px-6 bg-white border-t">
      <div class="max-w-6xl mx-auto text-center mb-12">
        <h2 class="text-3xl font-bold">Perks & Benefits</h2>
        <p class="text-gray-600 mt-4">
          We take care of our team so you can do your best work.
        </p>
      </div>
      <div class="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto text-left">
        <div class="bg-gray-50 p-6 rounded-xl shadow">
          <h3 class="text-lg font-semibold text-blue-700 mb-2">
            Flexible Hours
          </h3>
          <p class="text-gray-600">
            Work when you’re most productive, no micromanagement.
          </p>
        </div>
        <div class="bg-gray-50 p-6 rounded-xl shadow">
          <h3 class="text-lg font-semibold text-blue-700 mb-2">
            Remote Friendly
          </h3>
          <p class="text-gray-600">
            Work from anywhere — we support async collaboration.
          </p>
        </div>
        <div class="bg-gray-50 p-6 rounded-xl shadow">
          <h3 class="text-lg font-semibold text-blue-700 mb-2">
            Learning Budget
          </h3>
          <p class="text-gray-600">
            Annual stipend for courses, books, and conferences.
          </p>
        </div>
      </div>
    </section>

    <!-- Catch-All CTA -->
    <section class="py-20 px-6 bg-blue-600 text-white text-center">
      <div class="max-w-3xl mx-auto">
        <h2 class="text-3xl font-bold mb-4">Don't see a role that fits?</h2>
        <p class="text-lg mb-8">
          We’re always open to great talent. Send us your resume anyway.
        </p>
        <router-link
          to="/apply"
          class="bg-white text-blue-600 font-semibold px-6 py-3 rounded-lg hover:bg-gray-100 transition"
        >
          Submit Resume
        </router-link>
      </div>
    </section>
  </main>
</template>

<script setup>
import HeroCard from "../../components/shared/HeroCard.vue";

// Icons from Lucide Vue
import { Code2, Server, Palette, Layers } from "lucide-vue-next";

const roles = [
  {
    title: "Frontend Developer",
    description:
      "Build modern, responsive web applications using Vue 3 and Tailwind CSS.",
    location: "Remote",
    type: "Full-time",
    icon: Code2,
  },
  {
    title: "Backend Engineer",
    description: "Design and maintain robust APIs using Python or Java.",
    location: "Toronto / Remote",
    type: "Full-time",
    icon: Server,
  },
  {
    title: "Product Designer",
    description:
      "Craft intuitive interfaces that delight users across platforms.",
    location: "Remote",
    type: "Contract",
    icon: Palette,
  },
  {
    title: "Full Stack Software Engineer",
    description:
      "Build responsive websites and design robust APIs using React and Python.",
    location: "Ottawa",
    type: "Full-time",
    icon: Layers,
  },
];
</script>
