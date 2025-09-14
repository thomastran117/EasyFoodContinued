<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div
      class="max-w-xl w-full bg-white p-8 sm:p-10 rounded-xl shadow-md text-center space-y-6"
    >
      <h1 class="text-3xl font-bold text-green-600">🎉 Order Confirmed!</h1>

      <p class="text-gray-700">
        Thank you for your order! We're getting it ready for you.
      </p>

      <p class="text-gray-600">
        Would you like to share your experience in a short optional survey?
      </p>

      <div class="flex flex-col sm:flex-row justify-center gap-4 pt-4">
        <router-link
          to="/survey"
          class="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition text-sm sm:text-base"
        >
          Fill Out Survey
        </router-link>
        <router-link
          to="/"
          class="bg-gray-100 text-gray-800 px-5 py-2 rounded-lg hover:bg-gray-200 transition text-sm sm:text-base"
        >
          Back to Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style scoped></style>
