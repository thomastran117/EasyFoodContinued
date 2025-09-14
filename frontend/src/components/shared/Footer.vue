<template>
  <footer class="bg-gray-900 text-gray-300">
    <div class="max-w-7xl mx-auto px-4 py-10 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
        <!-- Logo and Description -->
        <div>
          <h3 class="text-xl font-bold text-white mb-2">EasyFood</h3>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            class="size-6"
          >
            <path
              d="M3.375 4.5C2.339 4.5 1.5 5.34 1.5 6.375V13.5h12V6.375c0-1.036-.84-1.875-1.875-1.875h-8.25ZM13.5 15h-12v2.625c0 1.035.84 1.875 1.875 1.875h.375a3 3 0 1 1 6 0h3a.75.75 0 0 0 .75-.75V15Z"
            />
            <path
              d="M8.25 19.5a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0ZM15.75 6.75a.75.75 0 0 0-.75.75v11.25c0 .087.015.17.042.248a3 3 0 0 1 5.958.464c.853-.175 1.522-.935 1.464-1.883a18.659 18.659 0 0 0-3.732-10.104 1.837 1.837 0 0 0-1.47-.725H15.75Z"
            />
            <path d="M19.5 19.5a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0Z" />
          </svg>

          <p class="text-sm text-gray-400">
            Making your digital experience better, every day.
          </p>
        </div>

        <!-- Navigation Links -->
        <div>
          <h4 class="font-semibold mb-3 text-white">Product</h4>
          <ul class="space-y-2 text-sm">
            <li>
              <a href="/restaurant" class="hover:text-white">Restaurants</a>
            </li>
            <li><a href="/services" class="hover:text-white">Services</a></li>
            <li><a href="#" class="hover:text-white">Solutions</a></li>
          </ul>
        </div>

        <div>
          <h4 class="font-semibold mb-3 text-white">Company</h4>
          <ul class="space-y-2 text-sm">
            <li><a href="/about" class="hover:text-white">About</a></li>
            <li><a href="/careers" class="hover:text-white">Careers</a></li>
            <li><a href="#" class="hover:text-white">Blog</a></li>
          </ul>
        </div>

        <div>
          <h4 class="font-semibold mb-3 text-white">Support</h4>
          <ul class="space-y-2 text-sm">
            <li><a href="/contact" class="hover:text-white">Contact Us</a></li>
            <li>
              <a href="/terms" class="hover:text-white">Term and Conditions</a>
            </li>
            <li>
              <a href="/faqs" class="hover:text-white"
                >Frequently Asked Questions</a
              >
            </li>
          </ul>
        </div>
      </div>

      <div
        class="mt-10 border-t border-gray-700 pt-6 flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0"
      >
        <p class="text-sm text-gray-500">
          &copy; 2025 EasyFood. All rights reserved.
        </p>
        <div class="flex space-x-4"></div>
      </div>
    </div>
  </footer>
</template>
