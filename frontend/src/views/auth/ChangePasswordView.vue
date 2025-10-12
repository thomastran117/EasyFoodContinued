<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import PublicApi from "../../api/PublicApi";

const router = useRouter();
const token = ref("");
const password = ref("");
const confirmPassword = ref("");
const error = ref("");
const success = ref("");
const showPw = ref(false);
const loading = ref(false);
const invalidToken = ref(false);

onMounted(() => {
  const params = new URLSearchParams(window.location.search);
  const t = params.get("token");
  if (!t) {
    error.value = "Missing or invalid reset token.";
    invalidToken.value = true;
  } else {
    token.value = t;
  }
});

const validate = () => {
  if (!password.value) return "Password is required.";
  if (password.value.length < 6)
    return "Password must be at least 6 characters long.";
  if (password.value !== confirmPassword.value)
    return "Passwords do not match.";
  return "";
};

const submit = async () => {
  error.value = "";
  success.value = "";
  const v = validate();
  if (v) return (error.value = v);

  try {
    loading.value = true;
    const res = await PublicApi.post(`/auth/change-password?token=${token.value}`,
      { password: password.value },
      { headers: { "Content-Type": "application/json" } }
    );

    success.value = res.data.message || "Password updated successfully!";
    setTimeout(() => router.push("/auth"), 2000);
  } catch (err) {
    const status = err.response?.status;

    if (status === 400) error.value = "Invalid or expired token.";
    else if (status === 401)
      error.value = "You are not authorized to perform this action.";
    else if (status === 404) error.value = "User account not found.";
    else
      error.value =
        err.response?.data?.detail ||
        "An unexpected error occurred. Please try again.";
  } finally {
    loading.value = false;
  }
};

const retry = () => {
  router.push("/forgot-password");
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4">
    <div
      class="w-full max-w-md bg-white rounded-xl shadow-md p-8 space-y-6 border border-gray-200"
    >
      <h1 class="text-2xl font-semibold text-gray-800 text-center">
        Change Your Password
      </h1>

      <p class="text-gray-500 text-sm text-center">
        Enter your new password below to reset your account.
      </p>

      <div v-if="error" class="text-red-600 text-sm text-center font-medium">
        {{ error }}
      </div>

      <div v-if="success" class="text-green-600 text-sm text-center font-medium">
        {{ success }}
      </div>

      <div v-if="!invalidToken && !success" class="space-y-4">
        <div>
          <label class="block text-gray-700 text-sm mb-1">New Password</label>
          <input
            :type="showPw ? 'text' : 'password'"
            v-model="password"
            placeholder="Enter new password"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-gray-700 text-sm mb-1"
            >Confirm Password</label
          >
          <input
            :type="showPw ? 'text' : 'password'"
            v-model="confirmPassword"
            placeholder="Confirm password"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div class="flex items-center space-x-2">
          <input
            id="showPw"
            type="checkbox"
            v-model="showPw"
            class="rounded text-blue-600 focus:ring-blue-500"
          />
          <label for="showPw" class="text-sm text-gray-700">Show password</label>
        </div>

        <button
          @click="submit"
          :disabled="loading"
          class="w-full bg-blue-600 text-white py-2.5 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-150 disabled:opacity-70"
        >
          {{ loading ? "Updating..." : "Update Password" }}
        </button>
      </div>

      <div v-if="invalidToken || error.includes('token')" class="text-center">
        <button
          @click="retry"
          class="mt-4 inline-block bg-gray-200 hover:bg-gray-300 text-gray-800 text-sm font-medium px-4 py-2 rounded transition-all"
        >
          Request New Link
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
input,
button {
  transition: all 0.2s ease;
}
</style>
