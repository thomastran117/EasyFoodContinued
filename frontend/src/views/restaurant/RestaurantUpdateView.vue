<template>
  <main class="min-h-screen bg-gray-50 text-gray-800 font-sans py-12 px-6">
    <section class="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow">
      <h1 class="text-2xl font-bold text-blue-600 mb-6">Update Restaurant</h1>

      <div v-if="loading" class="text-gray-500 mb-4">
        Loading restaurant data...
      </div>
      <div v-if="error" class="text-red-500 mb-4">
        Error: {{ errorMessage }}
      </div>

      <RestaurantForm
        v-if="!loading && !error"
        :initialData="form"
        :loading="submitLoading"
        :error="submitError"
        :errorMessage="submitErrorMessage"
        :success="submitSuccess"
        successMessage="Restaurant updated successfully!"
        submitLabel="Update Restaurant"
        submitLabelLoading="Updating..."
        @submit="handleSubmit"
      />
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";
import { useAuth } from "../../composables/useAuth";
import RestaurantForm from "../../components/restaurant/RestaurantForm.vue";

const props = defineProps({ link: String });
const route = useRoute();
const auth = useAuth();

const loading = ref(false);
const error = ref(false);
const errorMessage = ref("");
const form = ref({
  name: "",
  description: "",
  location: "",
  logoUrl: "",
});

const submitLoading = ref(false);
const submitSuccess = ref(false);
const submitError = ref(false);
const submitErrorMessage = ref("");

onMounted(async () => {
  loading.value = true;
  error.value = false;
  errorMessage.value = "";
  try {
    const res = await axios.get(`${props.link}/api/restaurant/user`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    });
    const data = res.data.restaurant;
    form.value = {
      name: data.name,
      description: data.description,
      location: data.location,
      logoUrl: data.logoUrl,
    };
  } catch (err) {
    error.value = true;
    errorMessage.value =
      err.response?.data?.message || "Failed to load restaurant";
  } finally {
    loading.value = false;
  }
});

const handleSubmit = async (formData) => {
  submitLoading.value = true;
  submitError.value = false;
  submitSuccess.value = false;
  submitErrorMessage.value = "";

  try {
    await axios.put(`http://localhost:8090/api/restaurant/`, formData, {
      headers: {
        Authorization: `Bearer ${auth.token}`,
        "Content-Type": "application/json",
      },
    });
    submitSuccess.value = true;
  } catch (err) {
    submitError.value = true;
    submitErrorMessage.value =
      err.response?.data?.message || "Failed to update restaurant.";
  } finally {
    submitLoading.value = false;
  }
};
</script>
