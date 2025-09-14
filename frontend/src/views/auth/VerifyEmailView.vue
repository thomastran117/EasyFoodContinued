<template>
  <div
    class="min-h-screen flex flex-col justify-center items-center bg-gray-50 px-4"
  >
    <div
      class="max-w-md w-full bg-white p-6 rounded shadow text-center space-y-6"
    >
      <h2 class="text-2xl font-semibold text-blue-700">Email Verification</h2>

      <div v-if="loading" class="text-blue-600">
        Verifying your email, please wait...
      </div>

      <div v-else-if="error" class="text-red-600">
        {{ error }}
        <div class="mt-4 space-x-2">
          <button
            @click="retry"
            class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-md"
          >
            Retry
          </button>
          <button
            @click="goToAuth"
            class="px-4 py-2 bg-gray-300 hover:bg-gray-400 text-black rounded-md"
          >
            Go to Login
          </button>
        </div>
      </div>

      <div v-else-if="success" class="text-green-600">
        {{ success }}
        <div class="mt-4">
          <button
            @click="goToAuth"
            class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md"
          >
            Continue to Login
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const loading = ref(true);
const error = ref(null);
const success = ref(null);
const router = useRouter();

const props = defineProps({
  link: String,
});

function getTokenFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("token");
}

async function verifyEmail(token) {
  loading.value = true;
  error.value = null;
  success.value = null;

  try {
    const response = await axios.get(`${props.link}/api/auth/verify`, {
      params: { token },
    });
    success.value = response.data.message || "Email verified successfully!";
  } catch (err) {
    error.value =
      err.response?.data?.detail || err.message || "Verification failed.";
  } finally {
    loading.value = false;
  }
}

function retry() {
  const token = getTokenFromUrl();
  if (token) {
    verifyEmail(token);
  }
}

function goToAuth() {
  router.push("/auth");
}

onMounted(() => {
  const token = getTokenFromUrl();
  if (!token) {
    loading.value = false;
    error.value = "Verification token not found in URL.";
    return;
  }
  verifyEmail(token);
});
</script>

<style scoped></style>
