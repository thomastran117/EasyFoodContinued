<template>
  <main class="min-h-screen bg-white text-black py-12 px-6">
    <section class="max-w-3xl mx-auto space-y-8">
      <h1 class="text-3xl font-bold text-blue-600">
        Frequently Asked Questions
      </h1>

      <div
        v-for="(faq, index) in faqs"
        :key="index"
        class="border-b border-gray-200"
      >
        <button
          @click="toggle(index)"
          class="w-full text-left py-4 flex justify-between items-center focus:outline-none"
        >
          <span class="text-lg font-semibold">
            {{ faq.question }}
          </span>
          <svg
            :class="{ 'rotate-180': faq.open }"
            class="w-5 h-5 text-blue-600 transition-transform duration-300"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>

        <transition name="fade">
          <div v-if="faq.open" class="pb-4 text-gray-700 text-base">
            {{ faq.answer }}
          </div>
        </transition>
      </div>
    </section>
  </main>
</template>

<script>
export default {
  name: "FAQView",
  data() {
    return {
      faqs: [
        {
          question: "How do I create an account?",
          answer:
            'Click on the "Sign Up" button at the top right and fill in your details.',
          open: false,
        },
        {
          question: "Can I change my email address later?",
          answer: "No, we currently do not support email changes.",
          open: false,
        },
        {
          question: "How do I contact support?",
          answer:
            "Email us at support@easyfood.com or fill out a contact form.",
          open: false,
        },
        {
          question: "Is my data secure?",
          answer:
            "Yes, we use industry-standard encryption to protect your information.",
          open: false,
        },
      ],
    };
  },
  methods: {
    toggle(index) {
      this.faqs[index].open = !this.faqs[index].open;
    },
  },
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
