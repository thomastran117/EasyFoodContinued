<template>
  <main class="min-h-screen bg-gray-50 text-gray-800 font-sans py-12 px-6">
    <section class="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow">
      <h1 class="text-2xl font-bold text-blue-600 mb-6">
        Create a New Restaurant
      </h1>
      <RestaurantForm
        :loading="loading"
        :error="error"
        :errorMessage="errorMessage"
        :success="success"
        successMessage="Restaurant created successfully!"
        submitLabel="Create Restaurant"
        submitLabelLoading="Creating..."
        @submit="handleSubmit"
      />
    </section>
  </main>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useAuth } from "../../composables/useAuth";
import RestaurantForm from "../../components/restaurant/RestaurantForm.vue";

const props = defineProps({ link: String });

const auth = useAuth();
const loading = ref(false);
const success = ref(false);
const error = ref(false);
const errorMessage = ref("");

const handleSubmit = async (formData) => {
  loading.value = true;
  error.value = false;
  success.value = false;
  errorMessage.value = "";

  try {
    await axios.post(`${props.link}/api/restaurant/`, formData, {
      headers: {
        Authorization: `Bearer ${auth.token}`,
        "Content-Type": "application/json",
      },
    });
    success.value = true;
  } catch (err) {
    error.value = true;
    errorMessage.value =
      err.response?.data?.message || "Failed to create restaurant.";
  } finally {
    loading.value = false;
  }
};
</script>
