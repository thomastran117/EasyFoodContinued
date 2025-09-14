<template>
  <main class="max-w-5xl mx-auto p-6 space-y-10">
    <div v-if="restaurantLoading" class="text-gray-500 text-center">
      Loading restaurant...
    </div>

    <div
      v-else-if="errorMessage"
      class="text-red-600 font-semibold text-center"
    >
      {{ errorMessage }}
    </div>

    <RestaurantDisplayCard v-else :restaurant="restaurant" />

    <FoodSearchBar
      :modelValue="query"
      @search="applyQuery"
      @reset="resetFilters"
    />

    <div v-if="foodLoading" class="text-gray-500 text-center">
      Loading food items...
    </div>
    <div v-else-if="error" class="text-red-600 font-semibold text-center">
      {{ error }}
    </div>
    <div v-else-if="foods.length === 0" class="text-gray-600 text-center">
      No food items found.
    </div>

    <FoodList
      v-else
      :foods="foods"
      :expandedFoods="expandedFoods"
      :cartItems="cart.foodList"
      @addToCart="handleAddToCart"
      @updateQty="handleQuantityChange"
      @toggle="toggleMore"
    />
    <div
      v-if="totalPages > 1"
      class="flex justify-center items-center gap-4 mt-8"
    >
      <button
        @click="currentPage--"
        :disabled="currentPage === 1"
        class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
      >
        Previous
      </button>

      <span class="text-sm text-gray-700 font-medium">
        Page {{ currentPage }} of {{ totalPages }}
      </span>

      <button
        @click="currentPage++"
        :disabled="currentPage === totalPages"
        class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
      >
        Next
      </button>
    </div>
  </main>
</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue";
import { useRoute } from "vue-router";
import { useCart } from "../../composables/useCart";
import FoodList from "../../components/food/FoodList.vue";
import FoodSearchBar from "../../components/food/FoodSearchBar.vue";
import RestaurantDisplayCard from "../../components/restaurant/RestaurantDisplayCard.vue";
import axios from "axios";

const props = defineProps({ link: String });

const cart = useCart();

const route = useRoute();
const restaurantId = route.params.id;
const currentPage = ref(1);
const limit = 6;
const total = ref(0);

const totalPages = computed(() => Math.ceil(total.value / limit));
const cartRestaurantId = computed(() => cart.restaurantId?.value || "");
const foods = ref([]);
const restaurant = ref(null);
const foodLoading = ref(true);
const restaurantLoading = ref(true);
const error = ref(null);
const errorMessage = ref("");

const expandedFoods = ref(new Set());

const query = ref({
  name: "",
  description: "",
  priceMin: null,
  priceMax: null,
  tags: "",
});

const handleSearch = () => {
  currentPage.value = 1;
  fetchFoods();
};

const resetFilters = () => {
  query.value = { name: "", description: "", price: null, tags: "" };
  currentPage.value = 1;
  fetchFoods();
};

const toggleMore = (id) => {
  if (expandedFoods.value.has(id)) {
    expandedFoods.value.delete(id);
  } else {
    expandedFoods.value.add(id);
  }
};

const handleAddToCart = (food) => {
  if (!cartRestaurantId.value || cartRestaurantId.value === restaurantId) {
    console.log(restaurant.value.name);
    cart.addToCart({
      id: food.id,
      name: food.name,
      price: food.price,
      image: food.foodUrl,
      quantity: 1,
      restaurant: restaurant.value.name,
    });
  } else {
    alert("You can only add items from one restaurant at a time.");
  }
};

const fetchRestaurant = async () => {
  restaurantLoading.value = true;
  error.value = null;
  errorMessage.value = "";

  try {
    const response = await axios.get(
      `${props.link}/api/restaurant/${restaurantId}`,
    );

    console.log(response.data);
    restaurant.value = response.data.restaurant || null;
  } catch (err) {
    error.value = true;
    errorMessage.value = err?.response?.status
      ? `Error ${err.response.status}: ${err.response.statusText}`
      : "Network error or server unavailable.";
  } finally {
    restaurantLoading.value = false;
  }
};

const fetchFoods = async () => {
  foodLoading.value = true;
  error.value = null;

  try {
    const res = await axios.get(
      `${props.link}/api/food/restaurant/${restaurantId}`,
      {
        params: {
          skip: (currentPage.value - 1) * limit,
          limit,
          ...(query.value.name && { name: query.value.name }),
          ...(query.value.description && {
            description: query.value.description,
          }),
          ...(query.value.priceMin && { priceMin: query.value.priceMin }),
          ...(query.value.priceMax && { priceMax: query.value.priceMax }),
          ...(query.value.tags && { tags: query.value.tags }),
        },
      },
    );

    foods.value = res.data.foods || [];
    total.value = res.data.total || 0;
  } catch (err) {
    error.value =
      err?.response?.data?.message || "Failed to load restaurant data.";
  } finally {
    foodLoading.value = false;
  }
};

const applyQuery = (newQuery) => {
  query.value = { ...newQuery };
  currentPage.value = 1;
  fetchFoods();
};

const handleQuantityChange = (id, qty) => {
  if (qty <= 0) {
    cart.removeFromCart(id);
  } else {
    cart.updateQuantity(id, qty);
  }
};

onMounted(() => {
  fetchRestaurant();
  fetchFoods();
});

watch(currentPage, fetchFoods);
watch(
  cartRestaurantId,
  (newVal) => {
    console.log("restaurantId updated:", newVal);
  },
  { immediate: true },
);
</script>

<style scoped>
.input {
  border: 1px solid #cbd5e1;
  padding: 0.5rem 0.75rem;
  border-radius: 0.75rem;
  font-size: 0.95rem;
  background-color: #f9fafb;
  width: 100%;
}
</style>
