<script setup>
import config from "../../config/envManager";

function base64URLEncode(str) {
  return btoa(String.fromCharCode.apply(null, new Uint8Array(str)))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

async function generateCodeChallenge(verifier) {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const digest = await crypto.subtle.digest("SHA-256", data);
  return base64URLEncode(digest);
}

async function handleMicrosoft() {
  const codeVerifier = crypto.randomUUID() + crypto.randomUUID();
  const codeChallenge = await generateCodeChallenge(codeVerifier);
  sessionStorage.setItem("ms_code_verifier", codeVerifier);

  const authUrl =
    `https://login.microsoftonline.com/common/oauth2/v2.0/authorize` +
    `?client_id=${config.ms_client}` +
    `&response_type=code` +
    `&redirect_uri=${encodeURIComponent(`${config.frontend_url}/auth/microsoft`)}` +
    `&response_mode=query` +
    `&scope=openid profile email offline_access` +
    `&code_challenge=${codeChallenge}` +
    `&code_challenge_method=S256`;

  window.location.href = authUrl;
}
</script>

<template>
  <button
    @click="handleMicrosoft"
    type="button"
    class="flex items-center justify-center w-1/2 py-3 rounded-xl font-medium transition-all duration-300 transform active:scale-95 bg-gray-500/40 backdrop-blur-md border border-gray-400 text-white shadow-md hover:bg-gray-400/50 hover:shadow-lg"
  >
    <svg
      class="h-5 w-5 mr-2"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 23 23"
    >
      <rect x="1" y="1" width="10" height="10" fill="#F25022" />
      <rect x="12" y="1" width="10" height="10" fill="#7FBA00" />
      <rect x="1" y="12" width="10" height="10" fill="#00A4EF" />
      <rect x="12" y="12" width="10" height="10" fill="#FFB900" />
    </svg>
    Microsoft
  </button>
</template>
