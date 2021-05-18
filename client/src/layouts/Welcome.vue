<template>
  <div :style="style" class="d-flex justify-center">
    <router-view />
  </div>
</template>
<script>
import { backgrounds } from "../helpers/constants/images"
export default {
  data() {
    return {
      style: {
        background: `url(${backgrounds.welcome})`,
        "background-size": "cover",
        "min-height": "100vh",
      },
    }
  },
}
</script>
