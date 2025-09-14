<template>
  <div class="max-w-5xl mx-auto p-6 space-y-8">
    <h1 class="text-2xl font-bold mb-4">Your Orders</h1>

    <div v-if="loading" class="text-gray-500">Loading your orders...</div>
    <div v-if="error" class="text-red-600 font-semibold">{{ error }}</div>

    <div v-if="orders.length === 0 && !loading && !error" class="text-gray-600">
      You have no orders yet.
    </div>

    <div
      v-for="order in orders"
      :key="order.id"
      class="border rounded-lg shadow p-6 bg-white"
    >
      <div class="flex justify-between items-center mb-4">
        <div>
          <p class="font-semibold">Order ID: {{ order.id }}</p>
          <p class="text-sm text-gray-500">
            Placed: {{ formatDate(order.created_at) }}
          </p>
        </div>
        <div class="text-right">
          <p class="font-semibold">Fulfillment:</p>
          <p>{{ capitalize(order.fulfillment_type) }}</p>
          <p class="text-sm">{{ order.address }}</p>
        </div>
      </div>

      <p class="mb-4 italic text-gray-700" v-if="order.notes">
        Notes: {{ order.notes }}
      </p>

      <div class="space-y-4">
        <div
          v-for="item in order.items"
          :key="item.id"
          class="flex items-center gap-4 border rounded-md p-3"
        >
          <img
            :src="item.image"
            alt="Food image"
            class="w-20 h-20 object-cover rounded-md"
            loading="lazy"
          />
          <div class="flex-1">
            <p class="font-semibold text-lg">{{ item.name }}</p>
            <p class="text-gray-600">Price: ${{ item.price.toFixed(2) }}</p>
            <p class="text-gray-600">Quantity: {{ item.quantity }}</p>
          </div>
          <div class="font-bold text-right text-lg">
            ${{ (item.price * item.quantity).toFixed(2) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useAuth } from "../../composables/useAuth";

const props = defineProps({
  link: String,
});

const auth = useAuth();
const orders = ref([]);
const loading = ref(false);
const error = ref("");

const fetchOrders = async () => {
  if (!auth.token) {
    error.value = "You must be logged in to view orders.";
    return;
  }
  loading.value = true;
  error.value = "";
  try {
    const res = await axios.get(`${props.link}/api/order/user`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    });
    orders.value = res.data.orders || [];
  } catch (err) {
    error.value =
      err.response?.data?.message || err.message || "Failed to load orders.";
  } finally {
    loading.value = false;
  }
};

const formatDate = (isoString) => {
  const date = new Date(isoString);
  return date.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const capitalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);

onMounted(fetchOrders);
</script>

<style scoped></style>
