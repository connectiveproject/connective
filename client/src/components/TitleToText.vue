<template>
  <p>
    <span class="font-weight-black">{{ title }}: </span><span>{{ text }}</span>
  </p>
</template>

<script>
export default {
  props: {
    title: {
      type: [String, Number],
      required: true,
    },
    text: {
      type: [String, Number],
      required: true,
    },
  },
}
</script>
