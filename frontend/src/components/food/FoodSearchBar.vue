<style>
/* Add this style block inside your component or global styles */
.modern-input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 2px solid #d1d5db; /* gray-300 */
  border-radius: 0.5rem; /* rounded-lg */
  background-color: #f9fafb; /* gray-50 */
  font-size: 1rem;
  transition:
    border-color 0.3s ease,
    box-shadow 0.3s ease;
  outline-offset: 2px;
}

.modern-input:focus {
  border-color: #2563eb; /* blue-600 */
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.4); /* subtle blue glow */
  background-color: white;
}
</style>

<template>
  <form
    @submit.prevent="onSubmit"
    class="bg-white p-4 rounded-xl border border-blue-200 shadow space-y-4 mb-6"
  >
    <input
      v-model="localQuery.name"
      placeholder="Search food name..."
      class="modern-input"
    />

    <div>
      <button
        type="button"
        @click="showAdvanced = !showAdvanced"
        class="text-sm text-blue-600 hover:underline"
      >
        {{ showAdvanced ? "Hide Filters ▲" : "More Filters ▼" }}
      </button>
    </div>

    <div v-if="showAdvanced" class="grid sm:grid-cols-2 gap-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1"
          >Description</label
        >
        <input
          v-model="localQuery.description"
          placeholder="e.g. spicy, vegan"
          class="modern-input"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Tags</label>
        <input
          v-model="localQuery.tags"
          placeholder="e.g. gluten-free, popular"
          class="modern-input"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1"
          >Min Price</label
        >
        <input
          v-model.number="localQuery.priceMin"
          type="number"
          min="0"
          placeholder="0"
          class="modern-input"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1"
          >Max Price</label
        >
        <input
          v-model.number="localQuery.priceMax"
          type="number"
          min="0"
          placeholder="100"
          class="modern-input"
        />
      </div>
    </div>

    <div class="flex justify-end gap-3 pt-2">
      <button
        type="submit"
        class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Search
      </button>
      <button
        type="button"
        @click="reset"
        class="px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
      >
        Reset
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, watch } from "vue";

const emit = defineEmits(["search", "reset"]);
const props = defineProps({ modelValue: Object });

const showAdvanced = ref(false);
const localQuery = ref({
  name: "",
  description: "",
  priceMin: null,
  priceMax: null,
  tags: "",
  ...props.modelValue,
});

watch(
  () => props.modelValue,
  (newVal) => {
    localQuery.value = { ...localQuery.value, ...newVal };
  },
  { deep: true },
);

const onSubmit = () => emit("search", { ...localQuery.value });
const reset = () => emit("reset");
</script>
