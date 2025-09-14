<template>
  <HeroCard
    title="Manage your Restaurant"
    subtitle="Modify your restaurant and items with our simple UI."
    :showButtons="false"
  />
  <div class="p-6 max-w-2xl mx-auto">
    <LoadingState v-if="loading" resource="your restaurant" />

    <!-- Error Component -->
    <ErrorState
      v-else-if="error"
      resource="your restaurant"
      :message="error"
      :on-retry="fetchRestaurant"
    />

    <!-- Create Prompt -->
    <CreatePrompt v-else-if="!restaurant" />

    <!-- Main Restaurant View -->
    <div v-else>
      <RestaurantCard :restaurant="restaurant" />
      <ManagePanel :restaurant-id="restaurant.id" @delete="showModal = true" />
    </div>

    <!-- Delete Modal -->
    <DeleteModal
      v-if="showModal"
      :restaurant="restaurant"
      @cancel="showModal = false"
      @confirm="deleteRestaurant"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import { useAuth } from "../../composables/useAuth";
import RestaurantCard from "../../components/restaurant/RestaurantUserCard.vue";
import ManagePanel from "../../components/restaurant/RestaurantManagePanel.vue";
import DeleteModal from "../../modals/RestaurantDeleteModal.vue";
import CreatePrompt from "../../components/restaurant/RestaurantCreatePrompt.vue";
import LoadingState from "../../components/shared/LoadingState.vue";
import ErrorState from "../../components/shared/ErrorState.vue";
import HeroCard from "../../components/shared/HeroCard.vue";

const props = defineProps({ link: String });

const restaurant = ref(null);
const loading = ref(true);
const error = ref(null);
const showModal = ref(false);
const auth = useAuth();

const fetchRestaurant = async () => {
  loading.value = true;
  error.value = null;

  try {
    const res = await axios.get(`${props.link}/api/restaurant/user`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    });
    restaurant.value = res.data.restaurant;
  } catch (err) {
    if (err.response?.status === 404) {
      restaurant.value = null;
    } else {
      error.value = err.message || "Something went wrong.";
    }
  } finally {
    loading.value = false;
  }
};

onMounted(fetchRestaurant);

const deleteRestaurant = async () => {
  try {
    await axios.delete(`${props.link}/api/restaurant/`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    });
    restaurant.value = null;
    showModal.value = false;
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to delete.";
    showModal.value = false;
  }
};
</script>
