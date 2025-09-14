<script setup>
defineProps({
  modelValue: String,
  disabled: Boolean,
});
const emit = defineEmits(["update:modelValue"]);
</script>

<template>
  <div>
    <label class="block font-medium mb-2">Order Notes</label>
    <textarea
      :value="modelValue"
      :disabled="disabled"
      class="w-full border rounded-lg p-3"
      rows="4"
      placeholder="Add delivery instructions, allergies, etc."
      @input="$emit('update:modelValue', $event.target.value)"
    ></textarea>
  </div>
</template>
