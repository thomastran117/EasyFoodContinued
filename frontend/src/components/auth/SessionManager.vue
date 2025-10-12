<script setup>
import { onMounted, ref } from "vue";
import PublicApi from "../../api/PublicApi";
import { useAuth } from "../../composables/useAuth";

const auth = useAuth();
const loading = ref(true);

const initSession = async () => {
  try {
    const res = await PublicApi.post(`/auth/refresh`);
    if (res.data?.email) {
      auth.setAuth({
        accessToken: res.data.token,
        email: res.data.email,
        userType: res.data.userType || null,
        avatar: res.data.avatar || null,
        role: res.data.role || null,
      });
    } else {
      auth.clearAuth();
    }
  } catch (err) {
    auth.clearAuth();
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  initSession();
});
</script>

<template>
  <div
    v-if="loading"
    class="flex justify-center items-center min-h-screen bg-white"
  >
    <div class="flex space-x-4">
      <div class="dot bg-black" style="animation-delay: 0s"></div>
      <div class="dot bg-black" style="animation-delay: 0.2s"></div>
      <div class="dot bg-black" style="animation-delay: 0.4s"></div>
    </div>
  </div>

  <slot v-else />
</template>

<style scoped>
.dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  opacity: 0.2;
  animation: pulse 1s infinite ease-in-out;
}

@keyframes pulse {
  0%,
  80%,
  100% {
    transform: scale(0.8);
    opacity: 0.2;
  }
  40% {
    transform: scale(1.3);
    opacity: 1;
  }
}
</style>
