<template>
  <div
    class="pt-16 absolute-bottom"
    v-intersect="{
      handler: onIntersect,
      options: { threshold: [0.1] },
    }"
  ></div>
</template>

<script>
export default {
  methods: {
    onIntersect(event) {
      if (event[0].isIntersecting) {
        this.$emit("end-of-page")
      }
    },
  },
}
</script>
