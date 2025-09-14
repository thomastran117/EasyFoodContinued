<template>
  <div class="mt-6 space-y-6">
    <h2 class="text-2xl font-bold text-green-800">Your Menu</h2>

    <div v-if="foods.length" class="grid gap-6">
      <div
        v-for="item in foods"
        :key="item.id"
        class="flex flex-col md:flex-row justify-between items-center gap-4 bg-white shadow-md rounded-2xl p-6 border border-gray-100 hover:shadow-lg transition fade-item"
      >
        <div class="flex-1 w-full">
          <h3 class="text-xl font-semibold text-green-700">{{ item.name }}</h3>
          <p class="text-gray-600 text-sm mt-1">{{ item.description }}</p>

          <div class="mt-3 space-y-1 text-sm text-gray-700">
            <p>💰 <strong>Price:</strong> ${{ item.price.toFixed(2) }}</p>
            <p v-if="item.calories !== null">
              🔥 <strong>Calories:</strong> {{ item.calories }}
            </p>
            <p v-if="item.ingredients">
              🧂 <strong>Ingredients:</strong> {{ item.ingredients }}
            </p>
            <p v-if="item.tags">🏷️ <strong>Tags:</strong> {{ item.tags }}</p>
          </div>

          <div class="flex gap-3 mt-4">
            <button
              @click="editingItem = item"
              class="px-4 py-1.5 rounded-xl bg-blue-600 text-white text-sm hover:bg-blue-700"
            >
              Update
            </button>

            <button
              @click="deletingItem = item"
              class="px-4 py-1.5 rounded-xl bg-red-500 text-white text-sm hover:bg-red-600"
            >
              Delete
            </button>
          </div>
        </div>

        <img
          :src="item.foodUrl"
          alt="Food Image"
          class="w-32 h-32 object-cover rounded-xl border shadow-sm"
        />
      </div>

      <FoodUpdateModal
        v-if="editingItem"
        :item="editingItem"
        :link="props.link"
        @close="editingItem = null"
      />

      <FoodDeleteModal
        v-if="deletingItem"
        :item="deletingItem"
        :link="props.link"
        @close="deletingItem = null"
      />
    </div>

    <p v-else class="text-gray-500 text-center text-sm">
      You haven't added any food items yet.
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import FoodDeleteModal from "../../modals/FoodDeleteModal.vue";
import FoodUpdateModal from "../../modals/FoodUpdateModal.vue";

const props = defineProps({
  foods: Array,
  link: String,
});

const emit = defineEmits(["edit", "delete"]);

const editingItem = ref(null);
const deletingItem = ref(null);

const handleUpdate = (updatedItem) => {
  emit("edit", updatedItem);
};

const handleDelete = (itemId) => {
  emit("delete", itemId);
};
</script>

<style scoped>
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
.fade-enter-active {
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
}
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-item {
  opacity: 0;
  animation: fadeInUp 0.5s forwards;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
  from {
    opacity: 0;
    transform: translateY(10px);
  }
}
</style>
