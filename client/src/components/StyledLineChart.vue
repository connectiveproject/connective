<template>
  <div class="wrapper">
    <line-chart v-bind="$attrs" />
  </div>
</template>

<script>
import LineChart from "./LineChart"
export default {
  inheritAttrs: false,
  components: { LineChart },
}
</script>

<style scoped>
.wrapper {
  max-width: 600px;
  margin: 150px auto;
}
</style>
