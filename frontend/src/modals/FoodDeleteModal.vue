<template>
  <div class="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
    <div class="bg-white rounded-2xl p-6 w-full max-w-sm shadow-xl text-center">
      <h2 class="text-xl font-semibold text-red-600">Delete Food Item</h2>
      <p class="text-gray-700 mt-2">
        Are you sure you want to delete <strong>{{ item.name }}</strong
        >?
      </p>

      <div class="flex justify-center gap-4 mt-6">
        <button @click="$emit('close')" class="btn border text-gray-600">
          Cancel
        </button>
        <button
          @click="confirmDelete"
          class="btn bg-red-600 text-white hover:bg-red-700"
        >
          Delete
        </button>
      </div>
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

const localItem = reactive({ ...props.item });
const emit = defineEmits(["close"]);
const loading = ref(false);
const auth = useAuth();

const confirmDelete = async () => {
  loading.value = true;
  try {
    await axios.delete(`${props.link}/api/food/${localItem.id}`, {
      headers: {
        Authorization: `Bearer ${auth.token}`,
      },
    });
    emit("close");
  } catch (err) {
    console.error("Delete failed:", err);
    alert("Failed to delete food item.");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.btn {
  padding: 0.5rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
}
</style>
