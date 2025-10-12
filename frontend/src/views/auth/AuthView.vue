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
          :style="{
            transform: isSignup ? 'translateX(-53.5%)' : 'translateX(0)',
          }"
        >
          <div class="absolute inset-0 overflow-hidden pointer-events-none">
            <div
              class="absolute inset-0 bg-gradient-to-br from-blue-200 via-pink-100 to-purple-200 opacity-80 animate-gradient-move"
            ></div>
            <svg
              class="absolute bottom-0 left-0 w-full h-[250px] opacity-80"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 1440 320"
              preserveAspectRatio="none"
            >
              <path
                fill="url(#formWaveGradient)"
                fill-opacity="1"
                d="M0,160L48,138.7C96,117,192,75,288,58.7C384,43,480,53,576,80C672,107,768,149,864,149.3C960,149,1056,107,1152,90.7C1248,75,1344,85,1392,90.7L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
              ></path>
              <defs>
                <linearGradient
                  id="formWaveGradient"
                  x1="0"
                  x2="1"
                  y1="0"
                  y2="1"
                >
                  <stop offset="0%" stop-color="#60a5fa" />
                  <stop offset="50%" stop-color="#a855f7" />
                  <stop offset="100%" stop-color="#ec4899" />
                </linearGradient>
              </defs>
            </svg>
            <svg
              class="absolute bottom-0 left-0 w-full h-[200px] opacity-40 animate-wave-slow"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 1440 320"
              preserveAspectRatio="none"
            >
              <path
                fill="url(#formWaveGradient)"
                fill-opacity="1"
                d="M0,192L40,186.7C80,181,160,171,240,144C320,117,400,75,480,64C560,53,640,75,720,101.3C800,128,880,160,960,176C1040,192,1120,192,1200,186.7C1280,181,1360,171,1400,165.3L1440,160L1440,320L1400,320C1360,320,1280,320,1200,320C1120,320,1040,320,960,320C880,320,800,320,720,320C640,320,560,320,480,320C400,320,320,320,240,320C160,320,80,320,40,320L0,320Z"
              ></path>
            </svg>
          </div>
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
<style scoped>
@keyframes wave {
  0% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(-15px);
  }
  100% {
    transform: translateX(0);
  }
}
.animate-wave-slow {
  animation: wave 12s ease-in-out infinite;
}
@keyframes gradientMove {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
.animate-gradient-move {
  background-size: 200% 200%;
  animation: gradientMove 10s ease infinite;
}
</style>
