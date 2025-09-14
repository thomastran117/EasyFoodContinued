<template>
  <main class="min-h-screen bg-gray-50 text-gray-800 font-sans">
    <HeroCard
      title="Get in Touch"
      subtitle="Have a question, idea, or just want to say hello? We'd love to hear from you."
      :showButtons="false"
    />

    <section class="py-16 px-6">
      <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-12">
        <form class="bg-white p-8 rounded-lg shadow-md space-y-6">
          <div>
            <label
              for="name"
              class="block text-sm font-medium text-gray-700 mb-1"
              >Name</label
            >
            <input
              id="name"
              type="text"
              class="w-full border border-gray-300 rounded-md p-3 focus:outline-none focus:ring focus:ring-blue-100"
              placeholder="Your name"
            />
          </div>
          <div>
            <label
              for="email"
              class="block text-sm font-medium text-gray-700 mb-1"
              >Email</label
            >
            <input
              id="email"
              type="email"
              class="w-full border border-gray-300 rounded-md p-3 focus:outline-none focus:ring focus:ring-blue-100"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label
              for="message"
              class="block text-sm font-medium text-gray-700 mb-1"
              >Message</label
            >
            <QuillEditor
              v-model:content="message"
              contentType="html"
              :options="editorOptions"
              style="height: 150px"
            />
          </div>
          <button
            type="submit"
            class="bg-blue-600 text-white px-6 py-3 rounded-md shadow hover:bg-blue-700 transition"
          >
            Send Message
          </button>
        </form>

        <div class="text-gray-700 space-y-6">
          <div>
            <h2 class="text-xl font-bold mb-2">Our Office</h2>
            <p>
              74 Innovation Drive<br />
              Ottawa, ON, K1A 100
            </p>
          </div>
          <div>
            <h2 class="text-xl font-bold mb-2">Email</h2>
            <a
              href="mailto:hello@example.com"
              class="text-blue-600 hover:underline"
              >support@easyfood.com</a
            >
          </div>
          <div>
            <h2 class="text-xl font-bold mb-2">Phone</h2>
            <p>1 800-555-7475</p>
          </div>
          <div>
            <h2 class="text-xl font-bold mb-2">Hours of Operation</h2>
            <p>
              Monday – Friday: 9:00 AM – 6:00 PM<br />
              Saturday: 10:00 AM – 4:00 PM<br />
              Sunday: Closed
            </p>
          </div>
          <div>
            <h2 class="text-xl font-bold mb-2">Follow Us</h2>
            <div class="flex gap-4 text-blue-600 text-xl">
              <a href="#" aria-label="Twitter" class="hover:text-blue-800">
                <TwitterIcon />
              </a>
              <a href="#" aria-label="LinkedIn" class="hover:text-blue-800">
                <LinkedinIcon />
              </a>
              <a href="#" aria-label="GitHub" class="hover:text-blue-800">
                <GithubIcon />
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import HeroCard from "../../components/shared/HeroCard.vue";
import { QuillEditor } from "@vueup/vue-quill";
import { ref } from "vue";

import {
  Twitter as TwitterIcon,
  Linkedin as LinkedinIcon,
  Github as GithubIcon,
} from "lucide-vue-next";

const message = ref("");

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
