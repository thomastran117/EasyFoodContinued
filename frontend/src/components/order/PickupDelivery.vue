<template>
  <div>
    <label class="block font-medium mb-2">Pickup or Delivery</label>
    <select
      v-model="fulfillmentType"
      :disabled="disabled"
      class="w-full border rounded-lg p-3"
    >
      <option disabled value="">Please select</option>
      <option value="pickup">Pickup</option>
      <option value="delivery">Delivery</option>
    </select>

    <div v-if="fulfillmentType === 'pickup'" class="mt-4">
      <label class="block font-medium mb-2">Select Pickup Location</label>
      <select
        v-model="selectedPickupLocation"
        class="w-full border rounded-lg p-3"
      >
        <option
          v-for="(location, index) in predefinedPickupLocations"
          :key="index"
          :value="location"
        >
          {{ location }}
        </option>
      </select>
    </div>

    <div v-if="fulfillmentType === 'delivery'" class="mt-4">
      <label class="block font-medium mb-2">Delivery Address</label>
      <input
        type="text"
        v-model="deliveryAddress"
        class="w-full border rounded-lg p-3"
        placeholder="Enter your delivery address"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  modelValue: String,
  disabled: Boolean,
  predefinedPickupLocations: {
    type: Array,
    default: () => [
      "123 Main St - Downtown Branch",
      "456 Oak Ave - Uptown Pickup",
      "789 Maple Rd - West Side",
    ],
  },
  selectedPickupLocationValue: String,
  deliveryAddressValue: String,
});

const emit = defineEmits([
  "update:modelValue",
  "update:selectedPickupLocationValue",
  "update:deliveryAddressValue",
]);

const fulfillmentType = ref(props.modelValue);
const selectedPickupLocation = ref(
  props.selectedPickupLocationValue || props.predefinedPickupLocations[0],
);
const deliveryAddress = ref(props.deliveryAddressValue || "");

watch(fulfillmentType, (val) => {
  emit("update:modelValue", val);
});

watch(selectedPickupLocation, (val) => {
  emit("update:selectedPickupLocationValue", val);
});

watch(deliveryAddress, (val) => {
  emit("update:deliveryAddressValue", val);
});
</script>
