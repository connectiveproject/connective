<template>
  <div :style="style" class="d-flex justify-center">
    <router-view />
  </div>
</template>
<script>
import { BACKGROUNDS } from "../helpers/constants/images"
export default {
  data() {
    return {
      style: {
        background: `url(${BACKGROUNDS.welcome})`,
        "background-size": "cover",
        "min-height": "100vh",
      },
    }
  },
}
</script>
