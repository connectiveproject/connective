// based on VueTribute (https://github.com/syropian/vue-tribute)

import Tribute from "tributejs"
// disable eslint for file
/* eslint-disable */
const VTribute =  {
  name: "v-tribute",
  props: {
    options: {
      type: Object,
      required: true
    }
  },
  watch: {
    options: {
      immediate: false,
      deep: true,
      handler() {
        if (this.tribute) {
          this.$nextTick(() => {
            const $el = this.$el.querySelectorAll("textarea")[0];
            console.log($el);
            this.tribute.detach($el);

            this.$nextTick(() => {
                const $el = this.$el.querySelectorAll("textarea")[0];
              this.tribute = new Tribute(this.options);
              this.tribute.attach($el);
              $el.tributeInstance = this.tribute;
            });
          });
        }
      }
    }
  },
  mounted() {
    if (typeof Tribute === "undefined") {
      throw new Error("[v-tribute] cannot locate tributejs!");
    }
    this.$nextTick(() => {
        const $el = this.$el.querySelectorAll("textarea")[0];
        this.tribute = new Tribute(this.options);

        this.tribute.attach($el);

        $el.tributeInstance = this.tribute;

        $el.addEventListener("tribute-replaced", e => {
          e.target.dispatchEvent(new Event("input", { bubbles: true }));
        });
    })



  },
  beforeDestroy() {
    const $el = this.$el.querySelectorAll("textarea")[0];

    if (this.tribute) {
      this.tribute.detach($el);
    }
  },
  render(h) {
    return h(
      "div",
      {
        staticClass: "v-tribute"
      },
      this.$slots.default
    );
  }
};

if (typeof window !== "undefined" && window.Vue) {
  window.Vue.component(VTribute.name, VTribute);
}
export default VTribute;
