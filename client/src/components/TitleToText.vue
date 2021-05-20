<template>
  <p>
    <span class="font-weight-black">{{ title }}: </span><span>{{ text }}</span>
  </p>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    text: {
      type: String,
      required: true,
    },
  },
}
</script>
