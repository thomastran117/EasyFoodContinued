<template>
  <div class="p-6 max-w-3xl mx-auto space-y-6">
    <ProgressBar
      :cart-items="cart.foodList.length"
      :has-notes="orderDetails.trim() !== ''"
      :has-fulfillment="fulfillmentType !== ''"
      :has-payment="paymentMethod !== ''"
    />

    <div v-if="cart.foodList.length === 0" class="text-gray-500">
      Your cart is empty.
    </div>

    <div
      v-for="step in steps"
      :key="step.key"
      class="border rounded-xl shadow overflow-hidden transition-all"
      :class="{
        'opacity-100': step.available,
        'opacity-50 cursor-not-allowed': !step.available,
      }"
    >
      <button
        class="w-full flex justify-between items-center px-4 py-3 text-left font-semibold text-lg bg-blue-100 hover:bg-blue-200 border-b border-blue-300 transition-all"
        :class="{
          'rounded-t-xl': true,
          'rounded-b-xl': !openSteps[step.key],
          'cursor-pointer': step.available,
          'cursor-not-allowed': !step.available,
        }"
        :disabled="!step.available"
        @click="
          () => {
            if (step.available) openSteps[step.key] = !openSteps[step.key];
            activeStep.value = step.key;
          }
        "
      >
        <span class="text-blue-900">{{ step.label }}</span>
        <svg
          :class="{ 'rotate-180': openSteps[step.key] }"
          class="w-5 h-5 transform transition-transform text-blue-700"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      <transition name="fade">
        <div v-if="openSteps[step.key]" class="px-4 py-4 bg-white border-t">
          <div v-if="step.key === 'cart'">
            <div
              v-for="(items, restaurantName) in groupedCart"
              :key="restaurantName"
              class="mb-6"
            >
              <h3 class="text-lg font-bold text-blue-700 mb-2">
                {{ restaurantName }}
              </h3>

              <div
                v-for="item in items"
                :key="item.id"
                class="flex items-center gap-4 border rounded-xl p-4 shadow-sm mb-4"
              >
                <img
                  :src="item.image"
                  alt="food image"
                  class="w-20 h-20 object-cover rounded-lg"
                />
                <div class="flex-1">
                  <h2 class="text-xl font-semibold">{{ item.name }}</h2>
                  <p class="text-sm text-gray-600">
                    ${{ item.price.toFixed(2) }} each
                  </p>
                  <div class="flex items-center mt-2 gap-2">
                    <button
                      class="bg-blue-500 text-white px-2 py-1 rounded"
                      @click="updateQuantity(item.id, item.quantity - 1)"
                    >
                      -
                    </button>
                    <span class="px-3">{{ item.quantity }}</span>
                    <button
                      class="bg-blue-500 text-white px-2 py-1 rounded"
                      @click="updateQuantity(item.id, item.quantity + 1)"
                    >
                      +
                    </button>
                    <button
                      class="ml-4 text-red-500 hover:underline"
                      @click="cart.removeFromCart(item.id)"
                    >
                      Remove
                    </button>
                  </div>
                </div>
                <div class="text-lg font-bold text-right">
                  ${{ (item.price * item.quantity).toFixed(2) }}
                </div>
              </div>
            </div>

            <div class="border-t pt-4 text-right">
              <p class="text-lg font-semibold">
                Total Items: {{ cart.totalItems }}
              </p>
              <p class="text-xl font-bold text-green-600">
                Total Price: ${{ cart.totalPrice.toFixed(2) }}
              </p>
            </div>
          </div>

          <div v-else-if="step.key === 'notes'">
            <OrderNotes v-model="orderDetails" :disabled="!canFillNotes" />
          </div>

          <div v-else-if="step.key === 'pickup'">
            <PickupDelivery
              v-model="fulfillmentType"
              :disabled="!canChooseFulfillment"
              :predefinedPickupLocations="predefinedPickupLocations"
              v-model:selectedPickupLocationValue="selectedPickupLocation"
              v-model:deliveryAddressValue="deliveryAddress"
            />
          </div>

          <div v-else-if="step.key === 'payment'">
            <PaymentMethod
              v-model="paymentMethod"
              :disabled="!canChoosePayment"
              v-model:paymentDetailsValue="paymentDetails"
            />
          </div>

          <div v-else-if="step.key === 'confirm'" class="text-right">
            <div v-if="!auth.token" class="text-red-600 font-semibold mb-4">
              Please
              <router-link
                to="/auth"
                class="underline text-blue-600 hover:text-blue-800"
                >log in</router-link
              >
              to place your order.
            </div>

            <button
              :disabled="!canPlaceOrder || !auth.token"
              @click="placeOrder"
              class="px-6 py-3 rounded-xl font-semibold transition text-white"
              :class="{
                'bg-green-600 hover:bg-green-700': canPlaceOrder && auth.token,
                'bg-gray-400 cursor-not-allowed': !canPlaceOrder || !auth.token,
              }"
            >
              Place Order
            </button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, watchEffect } from "vue";
import { useCart } from "../../composables/useCart";
import { useAuth } from "../../composables/useAuth";
import ProgressBar from "../../components/order/ProgressBar.vue";
import OrderNotes from "../../components/order/OrderNotes.vue";
import PickupDelivery from "../../components/order/PickupDelivery.vue";
import PaymentMethod from "../../components/order/PaymentMethod.vue";
import axios from "axios";
import { useRouter } from "vue-router";

const props = defineProps({
  link: String,
});

const predefinedPickupLocations = [
  "123 Main St - Downtown Branch",
  "456 Oak Ave - Uptown Pickup",
  "789 Maple Rd - West Side",
];

const cart = useCart();
const auth = useAuth();
const router = useRouter();

const activeStep = ref("cart");
const openSteps = ref({
  cart: true,
  notes: false,
  pickup: false,
  payment: false,
  confirm: false,
});

const orderDetails = ref("");
const fulfillmentType = ref("");
const paymentMethod = ref("");
const paymentDetails = ref({
  name: "",
  cardNumber: "",
  expiry: "",
  cvv: "",
});

const steps = computed(() => [
  {
    key: "cart",
    label: "Cart Items",
    available: cart.foodList.length > 0,
  },
  {
    key: "notes",
    label: "Order Notes",
    available: canFillNotes.value,
  },
  {
    key: "pickup",
    label: "Pickup/Delivery",
    available: canChooseFulfillment.value,
  },
  {
    key: "payment",
    label: "Payment Method",
    available: canChoosePayment.value,
  },
  {
    key: "confirm",
    label: "Confirm & Place Order",
    available: canPlaceOrder.value,
  },
]);

const selectedPickupLocation = ref(predefinedPickupLocations[0]);
const deliveryAddress = ref("");

const canFillNotes = computed(() => cart.foodList.length > 0);
const canChooseFulfillment = computed(
  () => canFillNotes.value && orderDetails.value.trim() !== "",
);
const canChoosePayment = computed(() => {
  return (
    canChooseFulfillment.value &&
    fulfillmentType.value !== "" &&
    ((fulfillmentType.value === "pickup" &&
      selectedPickupLocation.value !== "") ||
      (fulfillmentType.value === "delivery" &&
        deliveryAddress.value.trim() !== ""))
  );
});

const canPlaceOrder = computed(() => {
  const details = paymentDetails.value;
  return (
    details.name.trim() !== "" &&
    details.cardNumber.trim() !== "" &&
    details.expiry.trim() !== "" &&
    details.cvv.trim().length !== ""
  );
});

const groupedCart = computed(() => {
  const groups = {};

  cart.foodList.forEach((item) => {
    const restaurant = item.restaurant || "Unknown Restaurant";
    if (!groups[restaurant]) groups[restaurant] = [];
    groups[restaurant].push(item);
  });

  return groups;
});

const updateQuantity = (id, quantity) => {
  cart.updateQuantity(id, quantity);
};

const placeOrder = async () => {
  const addressInfo =
    fulfillmentType.value === "pickup"
      ? { type: "pickup", address: selectedPickupLocation.value }
      : { type: "delivery", address: deliveryAddress.value };

  const paymentInfo = {
    type: paymentMethod.value,
    ...paymentDetails.value,
  };

  const payload = {
    items: cart.foodList.map((item) => ({
      food_id: item.id,
      quantity: item.quantity,
    })),
    notes: orderDetails.value,
    fulfillment: addressInfo,
    payment: paymentInfo,
  };

  try {
    const response = await axios.post(`${props.link}/api/order/`, payload, {
      headers: {
        Authorization: `Bearer ${auth.token}`,
        "Content-Type": "application/json",
      },
    });

    cart.clearCart();

    router.push("/order/confirmation");
  } catch (error) {
    console.error(
      "Failed to place order:",
      error.response?.data || error.message,
    );
  }
};

watchEffect(() => {
  if (canFillNotes.value) openSteps.value.notes = true;
  if (canChooseFulfillment.value) openSteps.value.pickup = true;
  if (canChoosePayment.value) openSteps.value.payment = true;
  if (canPlaceOrder.value) openSteps.value.confirm = true;
});
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  max-height: 0;
  overflow: hidden;
}
.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  max-height: 500px;
  overflow: hidden;
}
</style>
