<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import { useAuth } from "../../composables/useAuth";
import config from "../../config/envManager";
const auth = useAuth();
const loading = ref(true);

const BACKEND_URL = config.backend_url;

onMounted(async () => {
  try {
    const res = await axios.post(
    `${BACKEND_URL}/api/auth/refresh`,
    {},
    { withCredentials: true }
    );

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
    console.warn("No active session:", err.message);
    auth.clearAuth();
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <slot v-if="!loading" />
</template>
