<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useAuth } from "../../composables/useAuth";
import config from "../../config/envManager";

const auth = useAuth();
const router = useRouter();
const backendUrl = config.backend_url;
const frontendUrl = config.frontend_url;

const status = ref("loading");
const message = ref("Signing you in with Microsoft…");

const retryLogin = () => {
  status.value = "loading";
  message.value = "Retrying Microsoft sign-in…";
  window.location.reload();
};

const goToAuth = () => {
  router.push("/auth");
};

onMounted(async () => {
  try {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");
    const verifier = sessionStorage.getItem("ms_code_verifier");

    if (!code || !verifier) {
      throw new Error("Missing authorization code or verifier.");
    }

    const tokenUrl = `https://login.microsoftonline.com/common/oauth2/v2.0/token`;
    const data = new URLSearchParams({
      client_id: config.ms_client,
      grant_type: "authorization_code",
      code,
      redirect_uri: `${frontendUrl}/auth/microsoft`,
      code_verifier: verifier,
    });

    const tokenResp = await axios.post(tokenUrl, data, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    const tokenResponse = tokenResp.data;
    const idToken = tokenResponse.id_token;
    if (!idToken) {
      throw new Error("No id_token returned from Microsoft.");
    }

    const backendResp = await axios.post(`${backendUrl}/api/auth/microsoft`, {
      id_token: idToken,
    });

    auth.setAuth({
      token: backendResp.data.token,
      email: backendResp.data.email,
    });

    status.value = "success";
    message.value = "Login successful! Redirecting…";

    setTimeout(() => {
      router.push("/restaurant");
    }, 1500);
  } catch (err) {
    console.error(err);
    status.value = "error";
    message.value = err.message || "Microsoft sign-in failed.";
  }
});
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-white to-sky-100 px-4"
  >
    <div
      class="w-full max-w-md bg-white shadow-xl rounded-2xl p-8 text-center flex flex-col items-center border border-gray-100"
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
            @click="retryLogin"
            class="px-5 py-2 rounded-full bg-blue-600 text-white font-medium hover:bg-blue-700 transition"
          >
            Retry
          </button>
          <button
            @click="goToAuth"
            class="px-5 py-2 rounded-full bg-gray-200 text-gray-700 font-medium hover:bg-gray-300 transition"
          >
            Back to Auth
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
