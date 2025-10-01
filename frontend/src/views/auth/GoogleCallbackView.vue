<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const status = ref("Completing Google sign-in...");
const router = useRouter();

onMounted(async () => {
  try {
    const hash = new URLSearchParams(window.location.hash.substring(1));
    const idToken = hash.get("id_token");

    if (!idToken) {
      status.value = "Error: No token from Google";
      return;
    }

    const res = await fetch("http://localhost:8050/api/auth/google", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_token: idToken }),
      credentials: "include",
    });

    if (!res.ok) throw new Error("Failed to exchange token");
    const data = await res.json();

    localStorage.setItem("app_token", data.token);

    status.value = "Login successful, redirecting...";
    router.push("/");
  } catch (err) {
    console.error(err);
    status.value = "Google sign-in failed";
  }
});
</script>

<template>
  <div>{{ status }}</div>
</template>
