<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
    <FoodCard
      v-for="food in foods"
      :key="food.id"
      :food="food"
      :expanded="expandedFoods.has(food.id)"
      :in-cart="!!cartMap[food.id]"
      :quantity="cartMap[food.id]?.quantity || 0"
      @toggle="toggleMore"
      @addToCart="$emit('addToCart', food)"
      @updateQty="(id, qty) => $emit('updateQty', id, qty)"
    />
  </div>
</template>

<script setup>
import FoodCard from "./FoodCard.vue";
import { computed } from "vue";

const props = defineProps({
  foods: Array,
  expandedFoods: Object,
  cartItems: Array,
});

const emit = defineEmits(["addToCart", "updateQty", "toggle"]);

const cartMap = computed(() => {
  if (!props.cartItems) return {};
  return props.cartItems.reduce((acc, item) => {
    acc[item.id] = item;
    return acc;
  }, {});
});

const toggleMore = (id) => {
  emit("toggle", id);
};
</script>
