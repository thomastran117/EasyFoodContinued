<template>
  <form @submit.prevent="onSubmit" class="space-y-5">
    <div>
      <label class="block font-medium mb-1">Name</label>
      <input
        v-model="localForm.name"
        type="text"
        required
        class="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <div>
      <label class="block font-medium mb-1">Description</label>
      <QuillEditor
        v-model:content="localForm.description"
        contentType="html"
        :options="editorOptions"
        style="height: 150px"
      />
    </div>

    <div>
      <label class="block font-medium mb-1">Location</label>
      <input
        v-model="localForm.location"
        type="text"
        required
        class="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <div>
      <label class="block font-medium mb-1">Logo URL</label>
      <input
        v-model="localForm.logoUrl"
        type="text"
        placeholder="https://example.com/logo.png"
        class="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <div v-if="localForm.logoUrl" class="mt-3">
        <img
          :src="localForm.logoUrl"
          alt="Logo Preview"
          class="max-h-40 rounded border border-gray-300 object-contain"
          @error="onImageError"
        />
      </div>
    </div>

    <button
      type="submit"
      :disabled="loading"
      class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
    >
      {{ loading ? submitLabelLoading : submitLabel }}
    </button>

    <div v-if="success" class="mt-4 text-green-600 font-medium">
      {{ successMessage }}
    </div>
    <div v-if="error" class="mt-4 text-red-500">Error: {{ errorMessage }}</div>
  </form>
</template>

<script setup>
import { reactive, toRefs, watch, ref } from "vue";
import { QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      name: "",
      description: "",
      location: "",
      logoUrl: "",
    }),
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: Boolean,
    default: false,
  },
  errorMessage: {
    type: String,
    default: "",
  },
  success: {
    type: Boolean,
    default: false,
  },
  successMessage: {
    type: String,
    default: "",
  },
  submitLabel: {
    type: String,
    default: "Submit",
  },
  submitLabelLoading: {
    type: String,
    default: "Submitting...",
  },
});

const emit = defineEmits(["submit"]);

const localForm = reactive({ ...props.initialData });

watch(
  () => props.initialData,
  (newVal) => {
    Object.assign(localForm, newVal);
  },
  { deep: true },
);

function onSubmit() {
  emit("submit", { ...localForm });
}

const onImageError = () => {};
const editorOptions = {
  theme: "snow",
  modules: {
    toolbar: [
      ["bold", "italic", "underline", "strike"],
      [{ header: 1 }, { header: 2 }],
      [{ list: "ordered" }, { list: "bullet" }],
      ["clean"],
    ],
  },
};
</script>
