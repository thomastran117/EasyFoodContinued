<script setup>
import config from "../../config/envManager";

function handleGoogle() {
  const scope = "openid email profile";
  const params = new URLSearchParams({
    client_id: config.google_client,
    redirect_uri: `${config.frontend_url}/auth/google`,
    response_type: "id_token",
    scope,
    nonce: crypto.randomUUID(),
    prompt: "select_account",
  });
  window.location.href = `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
}
</script>

<template>
  <button
    @click="handleGoogle"
    type="button"
    class="flex items-center justify-center w-1/2 py-3 rounded-xl font-medium transition-all duration-300 transform active:scale-95 bg-gray-500/40 backdrop-blur-md border border-gray-400 text-white shadow-md hover:bg-gray-400/50 hover:shadow-lg"
  >
    <svg
      class="h-5 w-5 mr-2"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 48 48"
      aria-hidden="true"
    >
      <path
        fill="#EA4335"
        d="M24 9.5c3.54 0 6.72 1.22 9.21 3.6l6.85-6.85C35.64 2.47 30.15 0 24 0 14.62 0 6.57 5.36 2.69 13.11l7.98 6.2C12.57 13.18 17.92 9.5 24 9.5z"
      />
      <path
        fill="#4285F4"
        d="M46.08 24.56c0-1.57-.14-3.07-.39-4.56H24v9.09h12.45c-.54 2.79-2.18 5.15-4.63 6.74l7.39 5.73c4.31-3.98 6.87-9.86 6.87-17z"
      />
      <path
        fill="#FBBC05"
        d="M10.67 28.31a14.48 14.48 0 0 1-.76-4.31c0-1.5.28-2.94.76-4.31l-7.98-6.2A23.88 23.88 0 0 0 0 24c0 3.82.91 7.42 2.69 10.51l7.98-6.2z"
      />
      <path
        fill="#34A853"
        d="M24 48c6.48 0 11.92-2.14 15.89-5.82l-7.39-5.73c-2.05 1.38-4.68 2.2-8.5 2.2-6.08 0-11.43-3.68-13.33-9.01l-7.98 6.2C6.57 42.64 14.62 48 24 48z"
      />
    </svg>
    Google
  </button>
</template>
