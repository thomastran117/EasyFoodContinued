<script setup>
import { ref } from "vue";
import { toast } from "vue3-toastify";
import {
  EnvelopeIcon,
  LockClosedIcon,
  EyeIcon,
  EyeSlashIcon,
} from "@heroicons/vue/24/outline";
import GoogleButton from "./GoogleButton.vue";
import MicrosoftButton from "./MicrosoftButton.vue";
import { useAuth } from "../../composables/useAuth";
import { useRouter } from "vue-router";
import PublicApi from "../../api/PublicApi";

const props = defineProps({
  isSignup: Boolean,
  loading: Boolean,
});
const emit = defineEmits(["update:loading", "toggleAuth"]);

const auth = useAuth();
const router = useRouter();

const email = ref("");
const password = ref("");
const rememberMe = ref(false);
const showPassword = ref(false);

const togglePassword = () => (showPassword.value = !showPassword.value);

async function handleSubmit() {
  emit("update:loading", true);
  try {
    const url = props.isSignup
      ? `/auth/signup`
      : `/auth/login`;

    const res = await PublicApi.post(url, {
      email: email.value,
      password: password.value,
      remember: rememberMe.value,
    });

    if (props.isSignup) {
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
  } finally {
    emit("update:loading", false);
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="space-y-5">
    <div class="relative">
      <EnvelopeIcon class="absolute left-3 top-3.5 h-5 w-5 text-gray-400" />
      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="w-full pl-10 pr-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
    </div>

    <div class="relative">
      <LockClosedIcon class="absolute left-3 top-3.5 h-5 w-5 text-gray-400" />
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

    <div v-if="!props.isSignup" class="flex items-center justify-between -mt-2">
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
        to="/auth/forgot-password"
        class="text-sm text-blue-600 hover:underline"
      >
        Forgot Password?
      </router-link>
    </div>

    <button
      type="submit"
      :disabled="props.loading"
      class="w-2/3 mx-auto block bg-blue-600 text-white py-4 rounded-full text-lg font-medium transition-all duration-200 transform hover:scale-105 hover:shadow-lg hover:bg-blue-700 active:scale-95"
    >
      {{
        props.loading
          ? "Please wait..."
          : props.isSignup
            ? "Create Account"
            : "Sign In"
      }}
    </button>

    <div class="flex items-center justify-center my-6">
      <div class="w-full h-[1.5px] bg-gray-500/60"></div>
      <span class="px-4 text-gray-700 text-sm font-semibold tracking-wide"
        >OR</span
      >
      <div class="w-full h-[1.5px] bg-gray-500/60"></div>
    </div>

    <div class="flex gap-4">
      <GoogleButton />
      <MicrosoftButton />
    </div>
  </form>
</template>
