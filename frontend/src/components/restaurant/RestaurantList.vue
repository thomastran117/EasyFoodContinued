<template>
  <transition-group
    name="fade"
    tag="div"
    class="grid gap-6 md:grid-cols-2 lg:grid-cols-3"
  >
    <RestaurantCard
      v-for="(restaurant, index) in restaurants"
      :key="restaurant.id"
      :restaurant="restaurant"
      :style="{ animationDelay: `${index * 150}ms` }"
      class="fade-item"
    />
  </transition-group>
</template>

<script setup>
import RestaurantCard from "./RestaurantCard.vue";

defineProps({
  restaurants: {
    type: Array,
    required: true,
  },
});
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
