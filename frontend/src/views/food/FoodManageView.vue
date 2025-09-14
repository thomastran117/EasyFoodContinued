<template>
  <HeroCard
    title="Manage your Food"
    subtitle="Modify your foods and items with our simple UI."
    :showButtons="false"
  />
  <div class="p-6 max-w-2xl mx-auto">
    <LoadingState v-if="loadingFood" resource="your foods" />

    <ErrorState
      v-else-if="error"
      resource="your foods"
      :message="errorFood"
      :on-retry="fetchFood"
    />

    <div class="flex justify-end mb-4">
      <button
        @click="router.push('/manage/create-food/')"
        class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg"
      >
        + Create Food
      </button>
    </div>

    <FoodManagePanel
      :link="props.link"
      :foods="food"
      @edit="updateFood"
      @delete="deleteFood"
    />

    <div
      v-if="food?.length"
      class="flex justify-center items-center gap-4 mt-6"
    >
      <button
        @click="currentPage--"
        :disabled="currentPage === 1"
        class="px-4 py-1.5 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
      >
        Previous
      </button>

      <span class="text-sm text-gray-600 font-medium">
        Page {{ currentPage }} of {{ totalPages }}
      </span>

      <button
        @click="currentPage++"
        :disabled="currentPage === totalPages"
        class="px-4 py-1.5 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import { useAuth } from "../../composables/useAuth";
import LoadingState from "../../components/shared/LoadingState.vue";
import ErrorState from "../../components/shared/ErrorState.vue";
import HeroCard from "../../components/shared/HeroCard.vue";
import FoodManagePanel from "../../components/food/FoodManagePanel.vue";
import { useRouter } from "vue-router";

const props = defineProps({ link: String });

const food = ref([]);
const loadingFood = ref(true);
const errorFood = ref(null);
const auth = useAuth();
const currentPage = ref(1);
const pageSize = 5;
const totalPages = ref(1);
const router = useRouter();

const fetchFood = async () => {
  loadingFood.value = true;
  errorFood.value = null;

  try {
    const res = await axios.get(`${props.link}/api/food/restaurant/user`, {
      headers: { Authorization: `Bearer ${auth.token}` },
      params: {
        skip: (currentPage.value - 1) * pageSize,
        limit: pageSize,
      },
    });

    food.value = res.data.foods;

    if (res.data.total !== undefined) {
      totalPages.value = Math.ceil(res.data.total / pageSize);
    }
  } catch (err) {
    if (err.response?.status === 404) {
      errorFood.value = "No food items found.";
    } else {
      errorFood.value = err.message || "Something went wrong.";
    }
  } finally {
    loadingFood.value = false;
  }
};

const updateFood = (updatedItem) => {
  const index = foods.value.findIndex((item) => item.id === updatedItem.id);
  if (index !== -1) {
    foods.value[index] = updatedItem;
  }
};

const deleteFood = (deletedItem) => {
  foods.value = foods.value.filter((item) => item.id !== deletedItem.id);
};

onMounted(fetchFood);

watch(currentPage, () => {
  fetchFood();
});
</script>
