<template>
  <v-hover v-slot="{ hover }">
    <div class="wrapper relative" :class="{ circle }">
      <slot />
      <v-btn
        @click="$emit('click')"
        :class="{ shadow }"
        color="blue-grey"
        v-show="hover"
        class="btn ma-2 white--text"
        fab
      >
        <v-icon dark>mdi-pencil</v-icon>
      </v-btn>
    </div>
  </v-hover>
</template>
<script>
export default {
  props: {
    circle: {
      type: Boolean,
      default: false,
    },
    shadow: {
      type: Boolean,
      default: true,
    },
  },
}
</script>
<style lang="scss" scoped>
$dark-light: rgba(0, 0, 0, 0.2);
.btn {
  z-index: 2;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.wrapper {
  width: fit-content;
  height: fit-content;
  overflow: hidden;
}
.circle {
  border-radius: 50%;
}
.shadow {
  -webkit-box-shadow: 0px 0px 26px 1000px $dark-light;
  -moz-box-shadow: 0px 0px 26px 1000px $dark-light;
  box-shadow: 0px 0px 26px 1000px $dark-light;
}
</style>
