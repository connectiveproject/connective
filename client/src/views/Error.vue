<template>
  <div
    :style="{ background: `url('${bg}')` }"
    class="error-bg d-flex justify-center align-center"
  >
    <v-col cols="11" sm="6" md="6" lg="5" xl="4">
      <v-card class="py-12 px-5 error-card" elevation="20" outlined>
        <v-card-title class="text-h3 justify-center mb-9"
          >{{ titleKey ? $t(titleKey) : $t("errors.oops") }}!</v-card-title
        >
        <v-card-text class="text-h5 text-center">{{
          bodyKey ? $t(bodyKey) : $t("errors.genericError")
        }}</v-card-text>
        <v-btn
          @click="$router.push({ path: '/' })"
          elevation="3"
          class="back-btn px-8 py-5"
        >
          {{ $t("general.homepage") }}
        </v-btn>
      </v-card>
    </v-col>
  </div>
</template>

<script>
import { BACKGROUNDS } from "../helpers/constants/images"
export default {
  props: {
    // i18n JSONs keys for title and body
    titleKey: String,
    bodyKey: String,
  },
  data() {
    return {
      bg: BACKGROUNDS.error,
    }
  },
}
</script>

<style lang="scss" scoped>
.error-bg {
  background-size: cover;
  min-height: 100vh;
}

.error-card {
  min-height: 350px;
  background-color: rgba(255, 255, 255, 0.9);
}

.back-btn {
  position: absolute;
  bottom: 60px;
  left: 50%;
  transform: translateX(-50%);
}
</style>
