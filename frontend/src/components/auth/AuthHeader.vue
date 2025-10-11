<template>
  <h1
    class="relative text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-purple-500 to-pink-500 text-center tracking-tight drop-shadow-md"
  >
    {{ isSignup ? "Create Account ✨" : "Login 👋" }}
    <span
      class="absolute left-1/2 -bottom-2 w-24 h-[3px] rounded-full bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 transform -translate-x-1/2 animate-pulse"
    ></span>
  </h1>
</template>

<script setup>
defineProps({ isSignup: Boolean });
</script>
