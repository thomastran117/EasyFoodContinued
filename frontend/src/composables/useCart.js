import { defineStore } from "pinia";
import { ref, computed, watch } from "vue";

export const useCart = defineStore("cart", () => {
  const foodList = ref([]);

  const loadCart = () => {
    const saved = localStorage.getItem("cart");
    if (saved) {
      const parsed = JSON.parse(saved);
      foodList.value = parsed.foodList || [];
    }
  };

  watch(
    [foodList],
    () => {
      localStorage.setItem(
        "cart",
        JSON.stringify({
          foodList: foodList.value,
        }),
      );
    },
    { deep: true },
  );

  const addToCart = (newItem) => {
    const existing = foodList.value.find((item) => item.id === newItem.id);

    if (existing) {
      existing.quantity += newItem.quantity || 1;
    } else {
      foodList.value.push({
        id: newItem.id,
        name: newItem.name,
        price: newItem.price,
        image: newItem.image,
        quantity: newItem.quantity || 1,
        restaurant: newItem.restaurant || "Unknown",
      });
    }
  };

  const removeFromCart = (id) => {
    foodList.value = foodList.value.filter((item) => item.id !== id);
  };

  const updateQuantity = (id, quantity) => {
    if (quantity <= 0) {
      removeFromCart(id);
    } else {
      const item = foodList.value.find((i) => i.id === id);
      if (item) {
        item.quantity = quantity;
      }
    }
  };

  const clearCart = () => {
    foodList.value = [];
  };

  const totalItems = computed(() =>
    foodList.value.reduce((total, item) => total + item.quantity, 0),
  );

  const totalPrice = computed(() =>
    foodList.value.reduce(
      (total, item) => total + item.price * item.quantity,
      0,
    ),
  );

  loadCart();

  return {
    foodList,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    totalItems,
    totalPrice,
  };
});
