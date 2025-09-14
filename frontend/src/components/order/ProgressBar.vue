<template>
  <div class="mb-10 relative">
    <!-- Base gray bar (only between nodes) -->
    <div
      class="absolute top-3 left-[10%] w-[80%] h-1 bg-gray-300 rounded-full z-0"
    ></div>

    <!-- Green fill bar (only between completed nodes) -->
    <div
      class="absolute top-3 left-[10%] h-1 bg-green-500 rounded-full z-10 transition-all duration-300"
      :style="{ width: fillPercent }"
    ></div>

    <!-- Step Nodes -->
    <div class="flex justify-between items-center relative z-20">
      <div
        v-for="(step, index) in steps"
        :key="index"
        class="flex flex-col items-center"
      >
        <div
          class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold"
          :class="{
            'bg-green-500 text-white': currentStep > index,
            'bg-blue-600 text-white': currentStep === index,
            'bg-gray-300 text-gray-700': currentStep < index,
          }"
        >
          {{ index + 1 }}
        </div>
        <div class="text-xs mt-2 text-center text-gray-600 w-24">
          {{ step.label }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  cartItems: { type: Number, required: true },
  hasNotes: { type: Boolean, required: true },
  hasFulfillment: { type: Boolean, required: true },
  hasPayment: { type: Boolean, required: true },
});

const steps = [
  { label: "Order" },
  { label: "Order Details" },
  { label: "Pickup/Delivery" },
  { label: "Payment" },
  { label: "Confirm" },
];

// Step index: 0 to 4 → 4 segments → 0%, 25%, 50%, 75%, 100%
const currentStep = computed(() => {
  if (props.cartItems === 0) return 0;
  if (!props.hasNotes) return 1;
  if (!props.hasFulfillment) return 2;
  if (!props.hasPayment) return 3;
  return 4;
});

// Total space between first and last node = 100% - 2 * 10% (left/right margin)
const fillPercent = computed(() => {
  const segmentPercent = 80 / (steps.length - 1); // 80% total bar width
  return `${segmentPercent * currentStep.value}%`;
});
</script>
