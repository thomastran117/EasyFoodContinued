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

const { apiUrl } = defineProps({
  apiUrl: {
    type: String,
    required: true,
  },
});

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
