<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useAuth } from "../../composables/useAuth";

const auth = useAuth();
const router = useRouter();
const apiUrl = "http://localhost:8050";

const loading = ref(true);
const error = ref(null);

const retryLogin = () => {
  loading.value = true;
  error.value = null;
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
      client_id: "6fbb3c76-8f8d-4280-87b5-ff2e23574279",
      grant_type: "authorization_code",
      code,
      redirect_uri: "http://localhost:3050/auth/microsoft",
      code_verifier: verifier,
    });

    const tokenResp = await axios.post(
      tokenUrl,
      data,
      {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      }
    );

    const tokenResponse = tokenResp.data;

    const idToken = tokenResponse.id_token;
    if (!idToken) {
      throw new Error("No id_token returned from Microsoft.");
    }

    const backendResp = await axios.post(`${apiUrl}/api/auth/microsoft`, {
      id_token: idToken,
    });

    auth.setAuth({
      token: backendResp.data.token,
      email: backendResp.data.email,
    });

    router.push("/restaurant");
  } catch (err) {
    error.value = err.message || "An unexpected error occurred.";
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="flex items-center justify-center h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100 px-4">
    <div
      class="backdrop-blur-md bg-white/70 shadow-2xl rounded-2xl p-8 max-w-md w-full text-center border border-gray-200"
    >
      <div v-if="loading" class="flex flex-col items-center space-y-4">
        <div class="relative w-12 h-12">
          <div class="absolute inset-0 border-4 border-blue-400 rounded-full animate-ping"></div>
          <div class="absolute inset-0 border-4 border-blue-600 rounded-full animate-spin border-t-transparent"></div>
        </div>
        <p class="text-gray-700 font-medium">Signing you in with Microsoft...</p>
      </div>

      <div v-else-if="error" class="space-y-6">
        <p class="text-red-600 font-semibold">
          ⚠️ Login failed
        </p>
        <p class="text-gray-600">{{ error }}</p>

        <div class="flex justify-center gap-4">
          <button
            @click="retryLogin"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
          >
            Retry
          </button>
          <button
            @click="goToAuth"
            class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg shadow hover:bg-gray-300 transition"
          >
            Return to Auth
          </button>
        </div>
      </div>

      <div v-else>
        <p class="text-green-600 font-medium">
          ✅ Login successful! Redirecting...
        </p>
      </div>
    </div>
  </div>
</template>
