<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import PublicApi from "../../api/PublicApi";

const loading = ref(true);
const error = ref(null);
const success = ref(null);
const router = useRouter();

function getTokenFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("token");
}

async function verifyEmail(token) {
  loading.value = true;
  error.value = null;
  success.value = null;

  try {
    const res = await PublicApi.get(`/auth/verify`, { params: { token } });
    success.value = res.data?.message || "Your email has been verified!";
  } catch (err) {
    error.value =
      err.response?.data?.detail ||
      err.message ||
      "Verification failed. Please try again.";
  } finally {
    loading.value = false;
  }
}

function retry() {
  const token = getTokenFromUrl();
  if (token) verifyEmail(token);
}

function goToAuth() {
  router.push("/auth");
}

onMounted(() => {
  const token = getTokenFromUrl();
  if (!token) {
    loading.value = false;
    error.value = "Verification token not found in the URL.";
    return;
  }
  verifyEmail(token);
});
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-white to-purple-100 px-4"
  >
    <div
      class="relative max-w-md w-full bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-8 text-center space-y-6"
    >
      <h1
        class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-purple-500 to-pink-500 drop-shadow-sm"
      >
        Email Verification ✉️
      </h1>

      <div
        v-if="loading"
        class="flex flex-col items-center justify-center py-6"
      >
        <div class="flex space-x-2 mb-4">
          <div
            class="h-3 w-3 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.3s]"
          ></div>
          <div
            class="h-3 w-3 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.15s]"
          ></div>
          <div class="h-3 w-3 bg-blue-500 rounded-full animate-bounce"></div>
        </div>
        <p class="text-blue-700 font-medium">
          Verifying your email, please wait...
        </p>
      </div>

      <div v-else-if="error" class="space-y-4">
        <div
          class="text-red-600 bg-red-100 rounded-lg py-3 px-4 font-medium border border-red-300"
        >
          {{ error }}
        </div>
        <div class="flex justify-center gap-3">
          <button
            @click="retry"
            class="px-5 py-2 bg-red-500 hover:bg-red-600 text-white rounded-full font-medium transition-all duration-200"
          >
            Retry
          </button>
          <button
            @click="goToAuth"
            class="px-5 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-full font-medium transition-all duration-200"
          >
            Go to Login
          </button>
        </div>
      </div>

      <div v-else-if="success" class="space-y-4">
        <div class="flex justify-center mb-2">
          <svg
            class="w-14 h-14 text-green-500"
            fill="none"
            stroke="currentColor"
            stroke-width="3"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
        <p class="text-green-700 font-medium text-lg">
          {{ success }}
        </p>
        <button
          @click="goToAuth"
          class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-full font-medium transition-all duration-200"
        >
          Continue to Login
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}
.animate-bounce {
  animation: bounce 1.4s infinite ease-in-out both;
}
</style>
