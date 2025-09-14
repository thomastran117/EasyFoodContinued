<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-gray-50 text-center px-6"
  >
    <h1 class="text-6xl font-bold text-blue-700">404</h1>
    <p class="text-xl mt-2 text-gray-700">
      Oops! The page you’re looking for doesn’t exist.
    </p>
    <p class="text-gray-500 mt-1">It may have been moved or deleted.</p>

    <router-link
      to="/"
      class="mt-6 inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
    >
      Go Home
    </router-link>
  </div>
</template>
