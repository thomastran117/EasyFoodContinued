<template>
  <div
    class="bg-white rounded-2xl shadow-md border border-blue-100 hover:shadow-lg transition overflow-hidden"
  >
    <img
      :src="food.foodUrl"
      :alt="food.name"
      class="w-full h-48 object-cover"
      @error="$event.target.src = fallbackUrl"
    />

    <div class="p-5">
      <h2 class="text-xl font-bold text-blue-800 mb-1">{{ food.name }}</h2>

      <p class="text-sm text-gray-600 mb-1">
        <span class="font-semibold">Price:</span> ${{ food.price.toFixed(2) }}
      </p>
      <p class="text-sm text-gray-700 mb-2 line-clamp-2">
        {{ food.description }}
      </p>

      <div class="mt-4 flex justify-between items-center">
        <button
          @click="$emit('toggle', food.id)"
          class="text-blue-600 hover:underline text-sm font-medium"
        >
          {{ expanded ? "Hide" : "More" }}
        </button>

        <div v-if="inCart">
          <div class="flex items-center gap-2">
            <button
              @click="$emit('updateQty', food.id, quantity - 1)"
              class="bg-gray-200 px-3 py-1 rounded text-sm"
            >
              −
            </button>
            <span class="text-sm font-semibold w-6 text-center">{{
              quantity
            }}</span>
            <button
              @click="$emit('updateQty', food.id, quantity + 1)"
              class="bg-gray-200 px-3 py-1 rounded text-sm"
            >
              +
            </button>
          </div>
        </div>

        <button
          v-else
          @click="$emit('addToCart', food)"
          class="bg-blue-600 text-white text-sm px-4 py-1.5 rounded-xl hover:bg-blue-700 transition"
        >
          Add to Cart
        </button>
      </div>

      <div v-if="expanded" class="mt-3 space-y-1 text-sm text-gray-600">
        <p>
          <span class="font-semibold">Calories:</span>
          {{ food.calories || "N/A" }}
        </p>
        <p>
          <span class="font-semibold">Ingredients:</span>
          {{ food.ingredients || "None listed" }}
        </p>
        <p><span class="font-semibold">Tags:</span> {{ food.tags || "—" }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  food: Object,
  expanded: Boolean,
  inCart: Boolean,
  quantity: Number,
});
const fallbackUrl = "https://via.placeholder.com/400x300?text=No+Image";
</script>
