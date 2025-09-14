<template>
  <div class="max-w-4xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-8 text-center text-blue-700">
      Create New Food
    </h1>
    <div
      class="mb-4 text-sm text-blue-800 bg-blue-50 border border-blue-200 rounded-lg p-4"
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
      @submit.prevent="submitFood"
      class="bg-white shadow-md rounded-2xl p-6 border border-blue-200 grid grid-cols-1 md:grid-cols-2 gap-6"
    >
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-semibold text-blue-800 mb-1"
            >Name</label
          >
          <input v-model="form.name" type="text" required class="input" />
        </div>

        <div>
          <label class="block text-sm font-semibold text-blue-800 mb-1"
            >Description</label
          >
          <textarea
            v-model="form.description"
            required
            class="input"
          ></textarea>
        </div>

        <div class="relative">
          <label class="block text-sm font-semibold text-blue-800 mb-1"
            >Price</label
          >
          <input
            v-model.number="form.price"
            type="number"
            step="0.01"
            min="0"
            required
            class="input pl-8"
          />
        </div>

        <div>
          <label class="block text-sm font-semibold text-blue-800 mb-1"
            >Image URL</label
          >
          <input v-model="form.foodUrl" type="url" required class="input" />
        </div>
      </div>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-semibold text-blue-800 mb-1"
            >Calories</label
          >
          <input v-model.number="form.calories" type="number" class="input" />
        </div>

        <div>
          <label class="block text-sm font-semibold text-blue-800 mb-1"
            >Tags (comma-separated)</label
          >
          <input
            v-model="form.tags"
            type="text"
            class="input"
            placeholder="e.g. sandwich, dinner"
          />
        </div>

        <div>
          <label class="block text-sm font-semibold text-blue-800 mb-1"
            >Ingredients (comma-separated)</label
          >
          <input
            v-model="form.ingredients"
            type="text"
            class="input"
            placeholder="e.g. sugar, flour, eggs"
          />
        </div>

        <div v-if="form.foodUrl" class="text-center">
          <img
            :src="form.foodUrl"
            alt="Food preview"
            class="rounded-xl max-h-64 mx-auto shadow border border-blue-200"
          />
        </div>
      </div>

      <div class="md:col-span-2">
        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-xl text-lg font-semibold"
        >
          Create Food
        </button>
        <p v-if="error" class="mt-4 text-red-600 font-medium text-center">
          {{ error }}
        </p>
        <p v-if="success" class="mt-4 text-green-600 font-medium text-center">
          Food created successfully!
        </p>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useAuth } from "../../composables/useAuth";
import { useRouter } from "vue-router";

const auth = useAuth();
const router = useRouter();

const props = defineProps({ link: String });

const form = ref({
  name: "",
  description: "",
  price: null,
  foodUrl: "",
  calories: null,
  tags: "",
  ingredients: "",
});

const tagInput = ref("");
const ingredientInput = ref("");
const isTagInputVisible = ref(false);
const isIngredientInputVisible = ref(false);

const addUniqueToArray = (arr, val) => {
  const trimmed = val.trim();
  if (trimmed && !arr.includes(trimmed)) arr.push(trimmed);
};

const confirmTag = () => {
  addUniqueToArray(form.value.tags, tagInput.value);
  tagInput.value = "";
  isTagInputVisible.value = false;
};

const confirmIngredient = () => {
  addUniqueToArray(form.value.ingredients, ingredientInput.value);
  ingredientInput.value = "";
  isIngredientInputVisible.value = false;
};

const removeTag = (index) => {
  form.value.tags.splice(index, 1);
};

const removeIngredient = (index) => {
  form.value.ingredients.splice(index, 1);
};

const error = ref(null);
const success = ref(false);

const submitFood = async () => {
  error.value = null;
  success.value = false;

  const payload = {
    name: form.value.name,
    description: form.value.description,
    price: form.value.price,
    foodUrl: form.value.foodUrl,
    calories: form.value.calories,
    tags: form.value.tags,
    ingredients: form.value.ingredients,
  };

  try {
    const response = await axios.post(`${props.link}/api/food/`, payload, {
      headers: {
        Authorization: `Bearer ${auth.token}`,
        "Content-Type": "application/json",
      },
    });

    success.value = true;
    setTimeout(() => router.push("/manage/manage-food"), 1000);
  } catch (err) {
    console.log(err);
    error.value = err.response?.data?.message || "Failed to create food.";
  }
};
</script>

<style scoped>
.input {
  border: 1px solid #bfd6f8;
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.75rem;
  font-size: 1rem;
  line-height: 1.5rem;
  background-color: #f9fbff;
}

.tag-input {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #bfd6f8;
  border-radius: 0.75rem;
  background-color: #f0f7ff;
}

.tag {
  background-color: #dbeafe;
  color: #1e40af;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  font-size: 0.875rem;
}

.tag.plus {
  background-color: #e0f2fe;
  color: #0369a1;
  cursor: pointer;
  font-weight: bold;
}

.tag.editing {
  padding: 0;
}

.tag .remove {
  margin-left: 0.5rem;
  cursor: pointer;
  font-weight: bold;
}

.tag-field {
  border: none;
  outline: none;
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
  background-color: transparent;
}
</style>
