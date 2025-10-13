<template>
  <VueRecaptcha
    ref="recaptcha"
    :sitekey="siteKey"
    size="invisible"
    @verify="onVerify"
    @expired="onExpired"
  />
</template>

<script setup>
import { ref, defineExpose, defineEmits } from "vue";
import { VueRecaptcha } from "vue3-recaptcha-v2";
import config from "../../config/envManager";

const siteKey = config.recaptcha_site_key;
const emit = defineEmits(["verified", "expired", "error"]);
const recaptcha = ref(null);

const onVerify = (token) => emit("verified", token);
const onExpired = () => emit("expired");

const execute = async () => {
  try {
    if (recaptcha.value && typeof recaptcha.value.execute === "function") {
      await recaptcha.value.execute();
    } else {
      throw new Error("reCAPTCHA instance not ready.");
    }
  } catch (e) {
    emit("error", e);
  }
};

defineExpose({ execute });
</script>
