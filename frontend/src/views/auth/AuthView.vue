<template>
  <div class="p-4 bg-yellow-100 border border-yellow-400 text-yellow-800 rounded mb-4">
    <p><strong>Demo Accounts:</strong></p>
    <ul class="list-disc list-inside">
      <li><code>test@test.com</code> / <code>test</code></li>
      <li><code>example@example.ca</code> / <code>example</code></li>
    </ul>
  </div>

  <AuthForm :apiUrl="props.link" />
</template>

<script setup>
import AuthForm from "../../components/auth/AuthForm.vue";

const props = defineProps({
  link: String,
});
</script>
