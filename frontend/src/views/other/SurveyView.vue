<template>
  <div
    class="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow space-y-6 border border-blue-200 relative"
  >
    <h2 class="text-2xl font-bold text-blue-700">EasyFood Feedback Survey</h2>

    <LoadingState v-if="loading" resource="feedback" />

    <ErrorState
      v-else-if="errorMessage"
      resource="feedback"
      :message="errorMessage.value"
      :on-retry="submitSurvey"
    />

    <div class="space-y-4">
      <div>
        <label class="block text-gray-800 font-medium mb-1"
          >What did you think of browsing our app?</label
        >
        <input
          type="text"
          v-model="answers.browsing"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:border-blue-400"
          placeholder="Was it easy to find what you were looking for?"
        />
      </div>

      <div>
        <label class="block text-gray-800 font-medium mb-1"
          >How smooth was the ordering process for you?</label
        >
        <input
          type="text"
          v-model="answers.ordering"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:border-blue-400"
          placeholder="Let us know if anything felt confusing or delightful!"
        />
      </div>

      <div>
        <label class="block text-gray-800 font-medium mb-1"
          >How would you describe the overall look and feel of EasyFood?</label
        >
        <input
          type="text"
          v-model="answers.design"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:border-blue-400"
          placeholder="Any thoughts on colors, layout, or vibe?"
        />
      </div>

      <div>
        <label class="block text-gray-800 font-medium mb-1"
          >Have any ideas or suggestions for us?</label
        >
        <textarea
          v-model="answers.suggestions"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:border-blue-400"
          rows="4"
          placeholder="We love fresh ideas and feedback!"
        />
      </div>
    </div>

    <div>
      <label class="block text-gray-800 font-medium mb-2"
        >How would you rate your overall experience today?</label
      >
      <div class="flex gap-2 flex-wrap">
        <button
          v-for="n in 10"
          :key="n"
          @click="answers.rating = n"
          :class="[
            'w-10 h-10 flex items-center justify-center rounded-full border transition',
            answers.rating === n
              ? 'bg-blue-600 text-white border-blue-600'
              : 'bg-white text-gray-800 border-gray-300 hover:bg-blue-100',
          ]"
          :aria-label="`Rate ${n} out of 10`"
        >
          {{ n }}
        </button>
      </div>
      <p class="text-sm text-gray-500 mt-2">1 = Not great, 10 = Amazing!</p>
    </div>

    <div class="text-right pt-4">
      <button
        @click="submitSurvey"
        :disabled="!isValid || loading"
        class="bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold transition hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="loading">Submitting...</span>
        <span v-else>Submit Feedback</span>
      </button>
    </div>

    <div
      v-if="success"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-30 z-50"
    >
      <div
        class="bg-white rounded-xl p-6 shadow-lg w-full max-w-sm text-center"
      >
        <h3 class="text-lg font-semibold text-green-700 mb-4">
          Feedback Sent!
        </h3>
        <p class="text-gray-700 mb-6">Thank you for sharing your thoughts.</p>
        <button
          @click="router.push('/')"
          class="bg-blue-600 text-white px-5 py-2 rounded-xl font-medium hover:bg-blue-700 transition"
        >
          Go Back Home
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useAuth } from "../../composables/useAuth";
import LoadingState from "../../components/shared/LoadingState.vue";
import ErrorState from "../../components/shared/ErrorState.vue";

const props = defineProps({
  link: String,
});

const router = useRouter();
const auth = useAuth();

const answers = ref({
  browsing: "",
  ordering: "",
  design: "",
  suggestions: "",
  rating: null,
});

const loading = ref(false);
const success = ref(false);
const errorMessage = ref(null);

const isValid = computed(
  () =>
    answers.value.browsing.trim() !== "" &&
    answers.value.ordering.trim() !== "" &&
    answers.value.design.trim() !== "" &&
    answers.value.rating !== null,
);

const submitSurvey = async () => {
  loading.value = true;
  errorMessage.value = null;

  try {
    await axios.post(
      `${props.link}/api/survey/`,
      { ...answers.value },
      {
        headers: {
          Authorization: `Bearer ${auth.token}`,
          "Content-Type": "application/json",
        },
      },
    );

    success.value = true;
  } catch (err) {
    console.error(err);
    errorMessage.value =
      err.response?.data?.message || "Something went wrong. Please try again.";
  } finally {
    loading.value = false;
  }
};
</script>
