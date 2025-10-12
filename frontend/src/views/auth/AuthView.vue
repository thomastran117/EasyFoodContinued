<script setup>
import { ref } from "vue";
import AuthHeader from "../../components/auth/AuthHeader.vue";
import AuthForm from "../../components/auth/AuthForm.vue";
import AuthSidePanel from "../../components/auth/AuthSidePanel.vue";

const isSignup = ref(false);
const transitioning = ref(false);
const loading = ref(false);

function toggleAuth() {
  if (loading.value) return;
  transitioning.value = true;
  setTimeout(() => {
    isSignup.value = !isSignup.value;
    setTimeout(() => (transitioning.value = false), 50);
  }, 250);
}

function handleLoading(val) {
  loading.value = val;
}
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-white to-purple-100"
  >
    <div
      class="relative w-full max-w-6xl h-[600px] bg-white/90 backdrop-blur-lg rounded-2xl shadow-2xl overflow-hidden"
    >
      <div class="relative w-full h-full">
        <div
          class="absolute w-[65%] h-full right-0 flex items-center justify-center p-10 bg-white/90 backdrop-blur-lg overflow-hidden transition-all duration-700 ease-in-out z-10"
          :style="{ transform: isSignup ? 'translateX(-53.5%)' : 'translateX(0)' }"
        >
          <div class="relative w-full max-w-lg space-y-6 z-10">
            <AuthHeader :isSignup="isSignup" />
            <AuthForm
              :isSignup="isSignup"
              :loading="loading"
              @update:loading="handleLoading"
              @toggleAuth="toggleAuth"
            />
          </div>
        </div>

        <AuthSidePanel
          :isSignup="isSignup"
          :transitioning="transitioning"
          :loading="loading"
          @toggleAuth="toggleAuth"
        />
      </div>
    </div>
  </div>
</template>
