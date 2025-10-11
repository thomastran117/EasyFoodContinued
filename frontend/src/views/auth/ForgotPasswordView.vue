<script setup>
import { ref } from "vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import config from "../../config/envManager";

const email = ref("");
const loading = ref(false);

async function handleForgotPassword() {
  if (!email.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    toast.error("Please enter a valid email address.");
    return;
  }

  loading.value = true;
  try {
    await axios.post(`${config.backend_url}/auth/forgot-password`, {
      email: email.value,
    });

    toast.info(
      "If there is an account associated with this email, you will receive a password reset link shortly."
    );
    email.value = "";
  } catch (err) {
    const status = err.response?.status;
    if (status === 400)
      toast.error("Invalid request. Please check your input and try again.");
    else if (status === 500)
      toast.error("Server error. Please try again later.");
    else
      toast.error(
        "Something went wrong while processing your request. Please try again later."
      );
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-white to-purple-100 px-4"
  >
    <div
      class="relative w-full max-w-md bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-8 space-y-6"
    >
      <div class="text-center space-y-3">
        <h1
          class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-purple-500 to-pink-500 drop-shadow-sm"
        >
          Forgot Password 🔐
        </h1>
        <p class="text-gray-600 text-base max-w-sm mx-auto">
          Enter your email address below, and if it matches an account, you’ll
          receive a link to reset your password.
        </p>
      </div>

      <form @submit.prevent="handleForgotPassword" class="space-y-5">
        <div>
          <label
            for="email"
            class="block text-gray-700 font-medium mb-2"
          >
            Email
          </label>
          <input
            v-model="email"
            id="email"
            type="email"
            placeholder="you@example.com"
            class="w-full py-3 px-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 transition-all text-gray-800"
            required
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 text-white py-3 rounded-full text-lg font-medium transition-all duration-200 transform hover:scale-105 hover:bg-blue-700 active:scale-95"
        >
          {{ loading ? "Sending..." : "Send Reset Link" }}
        </button>

        <div class="text-center">
          <router-link
            to="/auth"
            class="text-sm text-blue-600 hover:underline font-medium"
          >
            Back to Login
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>
