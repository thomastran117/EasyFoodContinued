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
            <h1
              class="relative text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-purple-500 to-pink-500 text-center tracking-tight drop-shadow-md"
            >
              {{ isSignup ? "Create Account ✨" : "Login 👋" }}

              <!-- Animated underline -->
              <span
                class="absolute left-1/2 -bottom-2 w-24 h-[3px] rounded-full bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 transform -translate-x-1/2 animate-pulse"
              ></span>
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

              <div
                v-if="!isSignup"
                class="flex items-center justify-between -mt-2"
              >
                <label
                  class="flex items-center gap-2 text-sm text-gray-600 cursor-pointer select-none"
                >
                  <input
                    type="checkbox"
                    v-model="rememberMe"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  Remember Me
                </label>
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
                class="w-2/3 mx-auto block bg-blue-600 text-white py-4 rounded-full text-lg font-medium transition-all duration-200 transform hover:scale-105 hover:shadow-lg hover:bg-blue-700 active:scale-95"
              >
                {{
                  loading
                    ? "Please wait..."
                    : isSignup
                      ? "Create Account"
                      : "Sign In"
                }}
              </button>

              <div class="flex items-center justify-center my-6">
                <div
                  class="w-full h-[1.5px] bg-gray-500/60 shadow-[0_0_4px_rgba(0,0,0,0.15)]"
                ></div>
                <span
                  class="px-4 text-gray-700 text-sm font-semibold tracking-wide"
                  >OR</span
                >
                <div
                  class="w-full h-[1.5px] bg-gray-500/60 shadow-[0_0_4px_rgba(0,0,0,0.15)]"
                ></div>
              </div>
              <div class="flex gap-4">
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
              class="border border-white text-white px-6 py-2 rounded-full transition-all duration-200 transform hover:scale-105 hover:bg-white hover:text-blue-600 active:scale-95"
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
import {
  EnvelopeIcon,
  LockClosedIcon,
  EyeIcon,
  EyeSlashIcon,
} from "@heroicons/vue/24/outline";
import { useAuth } from "../../composables/useAuth";
import { useRouter } from "vue-router";
import config from "../../config/envManager";

const apiUrl = config.backend_url;
const auth = useAuth();
const showPassword = ref(false);
const isSignup = ref(false);
const transitioning = ref(false);
const email = ref("");
const password = ref("");
const rememberMe = ref(false);
const loading = ref(false);
const router = useRouter();

const togglePassword = () => (showPassword.value = !showPassword.value);

function toggleAuth() {
  if (loading.value) return;
  transitioning.value = true;
  setTimeout(() => {
    isSignup.value = !isSignup.value;
    setTimeout(() => (transitioning.value = false), 50);
  }, 250);
}

async function handleGoogle() {
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

async function handleSubmit() {
  loading.value = true;
  try {
    const url = isSignup.value
      ? `${apiUrl}/api/auth/signup`
      : `${apiUrl}/api/auth/login`;

    const res = await axios.post(url, {
      email: email.value,
      password: password.value,
      rememberMe: rememberMe.value,
    });

    if (isSignup.value) {
      toast.success("Verification sent to your email. Please validate.");
    } else {
      toast.success("Logged in successfully!");
      auth.setAuth({
        accessToken: res.data.token,
        email: res.data.email,
      });
      router.push("/restaurant");
    }
  } catch (err) {
    const status = err.response?.status;
    if (status === 400) toast.error("Invalid input. Please check your form.");
    else if (status === 401)
      toast.error("Invalid credentials. Please try again.");
    else if (status === 409)
      toast.error("Email already in use. Try logging in instead.");
    else if (status === 500)
      toast.error("Server error. Please try again later.");
    else toast.error(err.response?.data?.message || "Something went wrong.");
    console.error(err);
  } finally {
    loading.value = false;
  }
}
</script>

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
