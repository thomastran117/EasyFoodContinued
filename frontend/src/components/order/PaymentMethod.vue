<template>
  <div>
    <label class="block font-medium mb-2">Payment Method</label>
    <select
      v-model="paymentMethod"
      :disabled="disabled"
      class="w-full border rounded-lg p-3"
    >
      <option disabled value="">Choose payment</option>
      <option value="credit">Credit Card</option>
      <option value="debit">Debit Card</option>
    </select>

    <div
      v-if="paymentMethod === 'credit' || paymentMethod === 'debit'"
      class="space-y-4 mt-4"
    >
      <div>
        <label class="block font-medium mb-1">Name on Card</label>
        <input
          v-model="paymentDetails.name"
          type="text"
          class="w-full border rounded-lg p-3"
          placeholder="Full name as on card"
        />
      </div>

      <div>
        <label class="block font-medium mb-1">Card Number</label>
        <input
          v-model="paymentDetails.cardNumber"
          type="text"
          class="w-full border rounded-lg p-3"
          placeholder="1234 5678 9012 3456"
          maxlength="19"
        />
      </div>

      <div class="flex gap-4">
        <div class="flex-1">
          <label class="block font-medium mb-1">Expiry</label>
          <input
            v-model="paymentDetails.expiry"
            type="text"
            class="w-full border rounded-lg p-3"
            placeholder="MM/YY"
            maxlength="5"
          />
        </div>

        <div class="flex-1">
          <label class="block font-medium mb-1">CVV</label>
          <input
            v-model="paymentDetails.cvv"
            type="text"
            class="w-full border rounded-lg p-3"
            placeholder="123"
            maxlength="4"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from "vue";

const props = defineProps({
  modelValue: String,
  disabled: Boolean,
  paymentDetailsValue: Object,
});

const emit = defineEmits(["update:modelValue", "update:paymentDetailsValue"]);

const paymentMethod = ref(props.modelValue);
const paymentDetails = reactive({
  name: "",
  cardNumber: "",
  expiry: "",
  cvv: "",
  ...props.paymentDetailsValue,
});

watch(paymentMethod, (val) => emit("update:modelValue", val));
watch(paymentDetails, (val) => emit("update:paymentDetailsValue", { ...val }), {
  deep: true,
});
</script>
