<template>
  <transition name="modal">
    <div class="modal-mask" data-testid="modal">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="text-h6 font-weight-bold text-center">
            <slot name="header">
              {{ $t("general.message") }}
            </slot>
          </div>

          <div class="mb-11 mt-5 mx-3 text-center">
            <slot>
              <!-- Default slot: body text -->
            </slot>
          </div>

          <v-btn class="d-block mx-auto" @click="onBtnClick" data-testid="modal-button">
            <slot name="btn">
              {{ $t("general.understood") }}
            </slot>
          </v-btn>
        </div>
      </div>
    </div>
  </transition>
</template>
<script>
export default {
  props: {
    redirectUrl: {
      // URL to redirect to on button click
      type: String,
      required: false,
    },
    redirectComponentName: {
      type: String,
      required: false,
    },
  },

  methods: {
    onBtnClick() {
      if (this.redirectUrl) {
        this.$router.push({ path: this.redirectUrl })
      } else if (this.redirectComponentName) {
        this.$router.push({ name: this.redirectComponentName })
      } else {
        this.$emit("close")
      }
    },
  },
}
</script>
<style lang="scss" scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: min(370px, 90vw);
  margin: 0px auto;
  padding: 20px 30px;
  background-color: white;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
}

// following are transition-related styling
.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>
