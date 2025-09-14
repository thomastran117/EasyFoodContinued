<template>
  <HeroCard
    title="Manage your Profile"
    subtitle="Customize to your desire"
    :showButtons="false"
  />
  <main class="min-h-screen bg-white text-black py-12 px-6">
    <section class="max-w-5xl mx-auto space-y-6">
      <LoadingState v-if="loading" resource="your profile" />
      <ErrorState
        v-else-if="error"
        resource="your profile"
        :message="errorMessage"
        :on-retry="fetchProfile"
      />

      <form
        v-else
        class="grid md:grid-cols-2 gap-8 bg-gray-50 p-6 rounded-lg shadow"
      >
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-blue-600 mb-1"
              >Email</label
            >
            <input
              type="email"
              v-model="user.email"
              disabled
              class="w-full border border-gray-300 rounded-md px-4 py-2 bg-gray-100 text-gray-700 cursor-not-allowed"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-blue-600 mb-1"
              >Username</label
            >
            <input
              type="text"
              v-model="user.username"
              class="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-blue-600 mb-1"
              >Phone</label
            >
            <input
              type="tel"
              v-model="user.phone"
              class="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-blue-600 mb-1"
              >Address</label
            >
            <input
              type="text"
              v-model="user.address"
              class="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <!-- Right Column -->
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-blue-600 mb-1"
              >Description</label
            >
            <QuillEditor
              v-model:content="user.description"
              contentType="html"
              :options="editorOptions"
              style="height: 150px"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-blue-600 mb-1"
              >Profile Image URL</label
            >
            <input
              type="text"
              v-model="user.profileUrl"
              class="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div class="text-center">
            <img
              :src="user.profileUrl || 'https://via.placeholder.com/150'"
              alt="Profile Image"
              class="w-32 h-32 mx-auto rounded-full object-cover border border-gray-300"
            />
            <p class="text-xs text-gray-500 mt-1">Preview</p>
          </div>
        </div>

        <!-- Submit Button (full width) -->
        <div class="md:col-span-2 flex justify-center mt-4">
          <button
            type="submit"
            class="bg-blue-600 text-white text-lg px-8 py-3 rounded-lg shadow hover:bg-blue-700 transition duration-200"
            @click.prevent="handleUpdate"
          >
            Save Changes
          </button>
        </div>
      </form>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useAuth } from "../../composables/useAuth";
import LoadingState from "../../components/shared/LoadingState.vue";
import ErrorState from "../../components/shared/ErrorState.vue";
import HeroCard from "../../components/shared/HeroCard.vue";

const props = defineProps({
  link: String,
});

const auth = useAuth();
const user = ref({});
const error = ref(null);
const loading = ref(true);

const fetchProfile = async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await axios.get(`${props.link}/api/user/`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    });
    user.value = res.data;
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load profile.";
  } finally {
    loading.value = false;
  }
};

const handleUpdate = async () => {
  try {
    await axios.put(`${props.link}/api/user/`, user.value, {
      headers: { Authorization: `Bearer ${auth.token}` },
    });
    alert("Profile updated successfully.");
  } catch (err) {
    alert("Failed to update profile.");
    console.error(err);
  }
};

onMounted(fetchProfile);

const editorOptions = {
  theme: "snow",
  modules: {
    toolbar: [
      ["bold", "italic", "underline", "strike"],
      [{ header: 1 }, { header: 2 }],
      [{ list: "ordered" }, { list: "bullet" }],
      ["clean"],
    ],
  },
};
</script>
