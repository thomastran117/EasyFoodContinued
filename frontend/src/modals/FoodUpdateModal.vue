<template>
  <div class="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
    <div
      class="bg-white rounded-2xl shadow-xl w-full max-w-3xl mx-4 max-h-[90vh] overflow-y-auto p-6 md:p-8"
    >
      <h2 class="text-2xl font-bold text-blue-700 mb-4 text-center">
        Update Food Item
      </h2>

      <div
        class="mb-6 text-sm text-blue-800 bg-blue-50 border border-blue-200 rounded-lg p-4"
      >
        <p class="font-semibold mb-1">Form Guidelines:</p>
        <ul class="list-disc list-inside space-y-1">
          <li>
            <span class="font-medium">Required:</span> Name, Description, Price,
            and Image URL
          </li>
          <li>
            <span class="font-medium">Optional:</span> Calories, Tags, and
            Ingredients
          </li>
        </ul>
      </div>

      <form
        @submit.prevent="handleSubmit"
        class="grid grid-cols-1 md:grid-cols-2 gap-6"
      >
        <div>
          <label class="block text-sm font-medium mb-1">Name *</label>
          <input v-model="localItem.name" class="input" type="text" required />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Price ($) *</label>
          <div class="relative">
            <span
              class="absolute left-3 top-1/2 transform -translate-y-1/2 text-blue-500 font-semibold"
              >$</span
            >
            <input
              v-model.number="localItem.price"
              class="input pl-8"
              type="number"
              step="0.01"
              min="0"
              required
            />
          </div>
        </div>

        <div class="md:col-span-2">
          <label class="block text-sm font-medium mb-1">Description *</label>
          <textarea
            v-model="localItem.description"
            class="input"
            rows="2"
            required
          ></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Calories</label>
          <input
            v-model.number="localItem.calories"
            class="input"
            type="number"
          />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Tags</label>
          <input v-model="localItem.tags" class="input" type="text" />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Ingredients</label>
          <input v-model="localItem.ingredients" class="input" type="text" />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Image URL *</label>
          <input
            v-model="localItem.foodUrl"
            class="input"
            type="url"
            required
          />
        </div>

        <div class="md:col-span-2">
          <label class="block text-sm font-medium mb-1">Image Preview</label>
          <img
            :src="localItem.foodUrl"
            alt="Preview"
            class="max-h-48 w-full object-contain border rounded-xl bg-gray-50"
          />
        </div>

        <div class="md:col-span-2 flex justify-end gap-3 pt-4">
          <button
            type="button"
            @click="$emit('close')"
            class="btn border border-gray-300 text-gray-700 hover:bg-gray-100"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="btn bg-blue-600 text-white hover:bg-blue-700"
            :disabled="loading"
          >
            <span v-if="loading">Saving...</span>
            <span v-else>Save</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import axios from "axios";
import { useAuth } from "../composables/useAuth";

const props = defineProps({
  item: Object,
  link: String,
});
const emit = defineEmits(["close"]);

const localItem = reactive({ ...props.item });
const loading = ref(false);
const auth = useAuth();

const handleSubmit = async () => {
  loading.value = true;
  try {
    await axios.put(`${props.link}/api/food/${localItem.id}`, localItem, {
      headers: {
        Authorization: `Bearer ${auth.token}`,
      },
    });
    emit("close");
  } catch (err) {
    console.error("Update failed:", err);
    alert("Failed to update food item.");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border-radius: 0.75rem;
  border: 1px solid #ccc;
  font-size: 1rem;
}

.btn {
  padding: 0.5rem 1.25rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition: background-color 0.2s ease;
}
</style>
