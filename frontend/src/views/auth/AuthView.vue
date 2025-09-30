<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-white to-purple-100"
  >
    <div
      class="relative w-full max-w-6xl h-[600px] bg-white/90 backdrop-blur-lg rounded-2xl shadow-2xl overflow-hidden"
    >
      <div class="relative w-full h-full">
        <div
          class="absolute w-[65%] h-full right-0 flex items-center justify-center p-10 bg-white transition-all duration-500 ease-in-out z-10"
          :style="{
            transform: isSignup ? 'translateX(-52%)' : 'translateX(0)',
          }"
        >
          <div class="w-full max-w-sm space-y-6">
            <h1 class="text-3xl font-bold text-gray-800 text-center">
              {{ isSignup ? "Sign Up" : "Login" }}
            </h1>
            <form @submit.prevent="handleSubmit" class="space-y-5">
              <div class="relative">
                <EnvelopeIcon
                  class="absolute left-3 top-3.5 h-5 w-5 text-gray-400"
                />
                <input
                  v-model="email"
                  type="email"
                  placeholder="Email"
                  class="w-full pl-10 pr-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div class="relative">
                <LockClosedIcon
                  class="absolute left-3 top-3.5 h-5 w-5 text-gray-400"
                />
                <input
                  :type="showPassword ? 'text' : 'password'"
                  v-model="password"
                  placeholder="Password"
                  class="w-full pl-10 pr-10 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
                <button
                  type="button"
                  @click="togglePassword"
                  class="absolute right-3 top-3.5 text-gray-500 hover:text-gray-700"
                >
                  <component
                    :is="showPassword ? EyeSlashIcon : EyeIcon"
                    class="h-5 w-5"
                  />
                </button>
              </div>

              <div v-if="!isSignup" class="text-right -mt-3">
                <router-link
                  to="/password"
                  class="text-sm text-blue-600 hover:underline"
                >
                  Forgot Password?
                </router-link>
              </div>

              <button
                type="submit"
                :disabled="loading"
                class="w-2/3 mx-auto block bg-blue-600 text-white py-4 rounded-full hover:bg-blue-700 transition text-lg font-medium"
              >
                {{
                  loading
                    ? "Please wait..."
                    : isSignup
                      ? "Create Account"
                      : "Sign In"
                }}
              </button>

              <div class="flex items-center justify-center my-4">
                <div class="w-full border-t border-gray-300"></div>
                <span class="px-3 text-gray-500 text-sm">OR</span>
                <div class="w-full border-t border-gray-300"></div>
              </div>

              <div class="flex gap-3">
                <button
                  @click="handleGoogle"
                  type="button"
                  class="flex items-center justify-center w-1/2 border border-gray-300 rounded-lg py-2 hover:bg-gray-50 transition"
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
                  <span class="text-gray-700 text-sm font-medium">Google</span>
                </button>

                <button
                  @click="handleMicrosoft"
                  type="button"
                  class="flex items-center justify-center w-1/2 border border-gray-300 rounded-lg py-2 hover:bg-gray-50 transition"
                >
                  <svg
                    class="h-5 w-5 mr-2"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 23 23"
                    aria-hidden="true"
                  >
                    <rect x="1" y="1" width="10" height="10" fill="#F25022" />
                    <rect x="12" y="1" width="10" height="10" fill="#7FBA00" />
                    <rect x="1" y="12" width="10" height="10" fill="#00A4EF" />
                    <rect x="12" y="12" width="10" height="10" fill="#FFB900" />
                  </svg>
                  <span class="text-gray-700 text-sm font-medium"
                    >Microsoft</span
                  >
                </button>
              </div>
            </form>
          </div>
        </div>

        <div
          class="absolute w-[35%] h-full left-0 flex items-center justify-center p-10 text-white transition-all duration-500 ease-in-out z-20"
          :class="
            isSignup
              ? 'bg-gradient-to-br from-purple-600 to-blue-500'
              : 'bg-gradient-to-br from-blue-500 to-purple-600'
          "
          :style="{
            transform: isSignup ? 'translateX(186%)' : 'translateX(0)',
          }"
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
              @click="toggleAuth"
              class="border border-white text-white px-6 py-2 rounded-full hover:bg-white hover:text-blue-600 transition"
              :disabled="loading"
            >
              {{ isSignup ? "Back to Login" : "Sign Up" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import { EnvelopeIcon, LockClosedIcon } from "@heroicons/vue/24/outline";
import { EyeIcon, EyeSlashIcon } from "@heroicons/vue/24/outline";
import { useAuth } from "../../composables/useAuth";
import { useRouter } from "vue-router";

const clientId = "6fbb3c76-8f8d-4280-87b5-ff2e23574279";
const tenant = "common";
const redirectUri = "http://localhost:3050/auth/callback";
const apiUrl = "http://localhost:8050";
const auth = useAuth();
const showPassword = ref(false);
const isSignup = ref(false);
const transitioning = ref(false);
const email = ref("");
const password = ref("");
const loading = ref(false);
const router = useRouter();

const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

function toggleAuth() {
  if (loading.value) return;
  transitioning.value = true;
  setTimeout(() => {
    isSignup.value = !isSignup.value;
    setTimeout(() => {
      transitioning.value = false;
    }, 50);
  }, 250);
}

async function handleGoogle() {
  console.log("Google pressed");
};


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

  const authUrl = `https://login.microsoftonline.com/${tenant}/oauth2/v2.0/authorize` +
    `?client_id=${clientId}` +
    `&response_type=code` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    `&response_mode=query` +
    `&scope=openid profile email offline_access` +
    `&code_challenge=${codeChallenge}` +
    `&code_challenge_method=S256`;

  window.location.href = authUrl;
}

async function handleSubmit() {
  loading.value = true;

  try {
    const url = isSignup.value
      ? `${apiUrl}/api/auth/signup`
      : `${apiUrl}/api/auth/login`;

    const res = await axios.post(url, {
      email: email.value,
      password: password.value,
    });

    if (isSignup.value) {
      toast.success("Verification sent to your email. Please validate.");
    } else {
      toast.success("Logged in successfully!");
      auth.setAuth({
        token: res.data.token,
        email: res.data.email,
      });
      router.push("/restaurant");
    }
  } catch (err) {
    const status = err.response?.status;

    if (status === 400) {
      toast.error("Invalid input. Please check your form.");
    } else if (status === 401) {
      toast.error("Invalid credentials. Please try again.");
    } else if (status === 409) {
      toast.error("Email already in use. Try logging in instead.");
    } else if (status === 500) {
      toast.error("Server error. Please try again later.");
    } else {
      toast.error(err.response?.data?.message || "Something went wrong.");
    }

    console.error(err);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped></style>
