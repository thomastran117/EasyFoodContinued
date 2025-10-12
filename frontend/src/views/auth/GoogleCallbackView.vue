<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import config from "../../config/envManager";
import { useAuth } from "../../composables/useAuth";
import axios from "axios";

const status = ref("loading");
const message = ref("Completing Google sign-in…");
const router = useRouter();
const backendUrl = config.backend_url;
const auth = useAuth();

async function handleGoogleCallback() {
  try {
    const hash = new URLSearchParams(window.location.hash.substring(1));
    const idToken = hash.get("id_token");

    if (!idToken) {
      status.value = "error";
      message.value = "Error: No token received from Google.";
      return;
    }

    const res = await axios.post(
      `${backendUrl}/auth/google`,
      { id_token: idToken },
      { withCredentials: true },
    );

    auth.setAuth({
      accessToken: res.data.token,
      email: res.data.email,
    });

    status.value = "success";
    message.value = "Login successful! Redirecting…";

    setTimeout(() => {
      router.push("/");
    }, 1500);
  } catch (err) {
    console.error(err);
    status.value = "error";
    message.value = "Google sign-in failed. Please try again.";
  }
}

function retry() {
  status.value = "loading";
  message.value = "Retrying Google sign-in…";
  handleGoogleCallback();
}

onMounted(handleGoogleCallback);
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-white to-sky-100"
  >
    <div
      class="w-full max-w-md bg-white shadow-xl rounded-2xl p-8 text-center flex flex-col items-center"
    >
      <div v-if="status === 'loading'" class="space-y-6">
        <div
          class="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto"
        ></div>
        <p class="text-gray-700 text-lg font-medium animate-pulse">
          {{ message }}
        </p>
      </div>

      <div v-else-if="status === 'success'" class="space-y-6">
        <svg
          class="w-16 h-16 text-green-500 mx-auto"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <p class="text-gray-800 text-lg font-semibold">{{ message }}</p>
      </div>

      <div v-else class="space-y-6">
        <svg
          class="w-16 h-16 text-red-500 mx-auto"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <p class="text-gray-800 text-lg font-semibold">{{ message }}</p>

        <div class="flex gap-4 justify-center">
          <button
            @click="retry"
            class="px-5 py-2 rounded-full bg-blue-600 text-white font-medium hover:bg-blue-700 transition"
          >
            Retry
          </button>
          <router-link
            to="/auth"
            class="px-5 py-2 rounded-full bg-gray-200 text-gray-700 font-medium hover:bg-gray-300 transition"
          >
            Back to Auth
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
