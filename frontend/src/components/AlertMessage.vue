<template>
  <p
    v-if="message"
    :class="['alert', `alert--${type}`]"
  >
    {{ message }}
  </p>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'error',
  },
})
</script>