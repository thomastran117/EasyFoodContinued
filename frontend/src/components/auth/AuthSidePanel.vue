<script setup>
defineProps({
  isSignup: Boolean,
  transitioning: Boolean,
  loading: Boolean,
});
const emit = defineEmits(["toggleAuth"]);
</script>

<template>
  <div
    class="absolute w-[35%] h-full left-0 flex items-center justify-center p-10 text-white transition-all duration-500 ease-in-out z-20"
    :class="isSignup
      ? 'bg-gradient-to-br from-purple-600 to-blue-500'
      : 'bg-gradient-to-br from-blue-500 to-purple-600'"
    :style="{ transform: isSignup ? 'translateX(186%)' : 'translateX(0)' }"
  >
    <div
      class="text-center transition-opacity duration-300"
      :class="{ 'opacity-0': transitioning || loading }"
    >
      <h2 class="text-3xl font-bold mb-4">
        {{ isSignup ? "Welcome Aboard 🚀" : "Welcome Back 👋" }}
      </h2>
      <p class="text-lg mb-6">
        {{
          isSignup
            ? "Let's get you started. Create your account below."
            : "We're happy to see you again. Login to continue."
        }}
      </p>
      <button
        @click="emit('toggleAuth')"
        class="border border-white text-white px-6 py-2 rounded-full transition-all duration-200 transform hover:scale-105 hover:bg-white hover:text-blue-600 active:scale-95"
        :disabled="loading"
      >
        {{ isSignup ? "Back to Login" : "Sign Up" }}
      </button>
    </div>
  </div>
</template>
