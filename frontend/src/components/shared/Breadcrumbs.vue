<template>
  <nav class="bg-white px-4 py-3 rounded-md w-full">
    <ol class="list-reset flex text-sm text-black">
      <li
        v-for="(crumb, index) in crumbs"
        :key="index"
        class="flex items-center"
      >
        <span v-if="index !== 0" class="mx-2 text-gray-400">/</span>

        <template v-if="index < crumbs.length - 1">
          <RouterLink
            :to="crumb.href"
            class="text-blue-600 hover:underline font-medium"
          >
            {{ crumb.label }}
          </RouterLink>
        </template>

        <template v-else>
          <span class="text-black font-semibold">{{ crumb.label }}</span>
        </template>
      </li>
    </ol>
  </nav>
</template>

<script>
export default {
  name: "Breadcrumb",
  props: {
    crumbs: {
      type: Array,
      required: true,
    },
  },
};
</script>
