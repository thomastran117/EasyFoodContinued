<template>
  <main class="min-h-screen bg-gray-50 text-gray-800 font-sans">
    <HeroCard
      title="About our Project"
      subtitle="We're passionate about building user-first applications that are modern, fast, and accessible."
      :showButtons="false"
    />

    <!-- Mission / Vision -->
    <section class="py-16 px-6">
      <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-12">
        <div>
          <h2 class="text-2xl font-bold mb-4 text-gray-800">Our Mission</h2>
          <p class="text-gray-600">
            To empower users by providing clean and simple UI that make food
            ordering faster and more approachable for everyone.
          </p>
        </div>
        <div>
          <h2 class="text-2xl font-bold mb-4 text-gray-800">Our Vision</h2>
          <p class="text-gray-600">
            To create a suite of tools and designs that simplify ordering
            without compromising quality or creativity.
          </p>
        </div>
      </div>
    </section>

    <!-- Team / Background -->
    <section class="py-16 bg-white px-6 border-t border-gray-200">
      <div class="max-w-4xl mx-auto text-center mb-12">
        <h2 class="text-3xl font-bold text-gray-800">Who We Are</h2>
        <p class="text-gray-600 mt-4">
          A small team of developers and designers who love building modern and
          innovative solutions
        </p>
      </div>

      <div class="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
        <div
          class="bg-gray-100 p-6 rounded-lg text-center shadow hover:shadow-md transition"
        >
          <img
            src="https://via.placeholder.com/100"
            alt="Team Member"
            class="rounded-full mx-auto mb-4"
          />
          <h3 class="text-xl font-semibold">Person 1</h3>
          <p class="text-sm text-gray-500">Developer</p>
        </div>
        <div
          class="bg-gray-100 p-6 rounded-lg text-center shadow hover:shadow-md transition"
        >
          <img
            src="https://via.placeholder.com/100"
            alt="Team Member"
            class="rounded-full mx-auto mb-4"
          />
          <h3 class="text-xl font-semibold">Person 2</h3>
          <p class="text-sm text-gray-500">UI/UX Designer</p>
        </div>
        <div
          class="bg-gray-100 p-6 rounded-lg text-center shadow hover:shadow-md transition"
        >
          <img
            src="https://via.placeholder.com/100"
            alt="Team Member"
            class="rounded-full mx-auto mb-4"
          />
          <h3 class="text-xl font-semibold">Person 3</h3>
          <p class="text-sm text-gray-500">Developer</p>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import HeroCard from "../../components/shared/HeroCard.vue";
</script>

<style scoped></style>
