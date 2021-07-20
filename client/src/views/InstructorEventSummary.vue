<template>
  <v-card
    class="my-15 mx-auto px-16 py-10"
    max-width="800"
    :elevation="$vuetify.breakpoint.mobile ? 0 : 3"
  >
    <v-card-title v-text="$t('events.eventSummary')" class="px-0" />
    <v-card-subtitle v-text="event.activityName" class="px-0 pt-3 pb-10" />
    <title-to-text
      :title="$t('groups.groupName')"
      :text="event.schoolGroupName || $t('errors.unavailable')"
    />
    <title-to-text
      :title="$t('time.startTime')"
      :text="parseDate(event.startTime) || $t('errors.unavailable')"
    />
    <title-to-text
      :title="$t('time.endTime')"
      :text="parseDate(event.endTime) || $t('errors.unavailable')"
    />
    <title-to-text
      :title="$t('myActivity.location')"
      :text="event.locationsName || $t('errors.empty')"
    />
    <form class="form" @submit.prevent="onSubmit">
      <v-row>
        <v-col cols="12">
          <vue-tribute :options="tributeOptions">
            <v-textarea
              :label="$t('events.summaryGeneralNotes')"
              v-model="summaryGeneralNotes"
              class="my-6"
            >
            </v-textarea>
          </vue-tribute>

        </v-col>
        <v-col cols="12" sm="12" lg="6">
          <v-select
            :items="consumerchoices"
            :label="$t('events.attendance')"
            v-model="attendedConsumers"
            class="my-6"
            multiple
            dense
          />
        </v-col>
        <v-col cols="12" sm="12" lg="6">
          <v-select
            :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
            v-model="summaryGeneralRating"
            :label="$t('events.summaryGeneralRating')"
            dense
            class="my-6"
          />
        </v-col>
        <v-col cols="12" sm="12" lg="6">
          <v-select
            :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
            v-model="summaryChildrenBehavior"
            :label="$t('events.summaryChildrenBehavior')"
            dense
            class="my-6"
          />
        </v-col>
      </v-row>
      <v-btn
        large
        type="submit"
        color="primary"
        class="mx-auto mt-9 mb-6 px-8"
        elevation="3"
        v-text="$t('userActions.save')"
      />
    </form>
    <modal
      redirectComponentName="InstructorUnsummarizedEvents"
      v-show="isModalOpen"
    >
      {{ modalMsg }}
    </modal>
  </v-card>
</template>

<script>
import { mapActions } from "vuex"
// import VueTribute from "vue-tribute"
import Tribute from "tributejs"
import debounce from "lodash/debounce"
import store from "../vuex/store"
import Utils from "../helpers/utils"
import TitleToText from "../components/TitleToText"
import Modal from "../components/Modal"
// disable eslint for file
/* eslint-disable */
const VueTribute = {
  name: "vue-tribute",
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
          setTimeout(() => {
            var $el = this.$slots.default[0].elm;
            console.log($el);
            this.tribute.detach($el);

            setTimeout(() => {
              $el = this.$slots.default[0].elm;
              this.tribute = new Tribute(this.options);
              this.tribute.attach($el);
              $el.tributeInstance = this.tribute;
            }, 0);
          }, 0);
        }
      }
    }
  },
  mounted() {
    if (typeof Tribute === "undefined") {
      throw new Error("[vue-tribute] cannot locate tributejs!");
    }

    const $el = document.querySelectorAll("textarea")[0];

    this.tribute = new Tribute(this.options);

    this.tribute.attach($el);

    $el.tributeInstance = this.tribute;

    $el.addEventListener("tribute-replaced", e => {
      e.target.dispatchEvent(new Event("input", { bubbles: true }));
    });
  },
  beforeDestroy() {
    const $el = document.querySelectorAll("textarea")[0];

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
  window.Vue.component(VueTribute.name, VueTribute);
}


export default {
  components: { TitleToText, Modal, VueTribute },
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  async beforeRouteEnter(to, from, next) {
    const event = await store.dispatch(
      "instructorEvent/getEvent",
      to.params.slug
    )
    const consumers = await store.dispatch(
      "instructorProgramGroup/getConsumers",
      event.schoolGroup
    )
    console.table(consumers);
    next(vm => {
      vm.event = event
      vm.consumerchoices = consumers.map(c => ({ text: c.name, value: c.slug }))
      vm.attendedConsumers = consumers.map(c => c.slug)
      vm.tributeOptions.values = consumers.map(consumer => {
        return {
          key: consumer.name,
          value: consumer.name.replace(" ", "_")
        };
      });
    })
  },
  data() {
    return {
      event: {},
      tributeOptions: {
        trigger: "@",
        values: [
          { key: "Collin Henderson", value: "syropian" },
          { key: "Sarah Drasner", value: "sarah_edo" },
          { key: "Evan You", value: "youyuxi" },
          { key: "Adam Wathan", value: "adamwathan" }
        ],
        positionMenu: true,
        menuContainer: document.querySelector(".menu-container")
      },
      consumerchoices: [],
      attendedConsumers: [],
      summaryGeneralNotes: "",
      summaryGeneralRating: 10,
      summaryChildrenBehavior: 10,
      modalMsg: this.$t("general.detailsSuccessfullyUpdated"),
      isModalOpen: false,
    }
  },
  methods: {
    ...mapActions("instructorEvent", ["updateEvent"]),
    parseDate: Utils.ApiStringToReadableDate,
    onSubmit: debounce(
      async function () {
        const data = {
          consumers: this.attendedConsumers,
          summaryGeneralNotes: this.summaryGeneralNotes,
          summaryGeneralRating: this.summaryGeneralRating,
          summaryChildrenBehavior: this.summaryChildrenBehavior,
          hasSummary: true,
        }
        await this.updateEvent({ slug: this.slug, data })
        this.isModalOpen = true
      },
      500,
      { leading: true, trailing: false }
    ),
  },
}
</script>
<style lang="scss">
  div.tribute-container > ul > li {
    -webkit-text-size-adjust: 100%;
    word-break: normal;
    tab-size: 4;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -webkit-tap-highlight-color: rgba(0,0,0,0);
    font-family: Roboto,sans-serif;
    text-align: center!important;
    box-sizing: inherit;
    align-items: center;
    cursor: default;
    display: inline-flex;
    line-height: 20px;
    max-width: 100%;
    outline: none;
    overflow: hidden;
    padding: 0 12px;
    position: relative;
    text-decoration: none;
    transition-duration: .28s;
    transition-property: box-shadow,opacity;
    transition-timing-function: cubic-bezier(.4,0,.2,1);
    vertical-align: middle;
    white-space: nowrap;
    margin: 8px!important;
    border-radius: 16px;
    font-size: 14px;
    height: 32px;
    background-color: #5cbbf6 !important;
    border-color: #5cbbf6 !important;
    color: #fff;
    background: #e0e0e0;
    // -webkit-text-size-adjust: 100%;
    // word-break: normal;
    // tab-size: 4;
    // text-rendering: optimizeLegibility;
    // -webkit-font-smoothing: antialiased;
    // -webkit-tap-highlight-color: rgba(0,0,0,0);
    // font-family: Roboto,sans-serif;
    // text-align: center!important;
    // cursor: default;
    // line-height: 20px;
    // white-space: nowrap;
    // font-size: 14px;
    // color: #fff;
    // background-repeat: no-repeat;
    // box-sizing: inherit;
    // padding: 0;
    // margin: 0;
    // align-items: center;
    // display: inline-flex;
    // height: 100%;
    // max-width: 100%;
   }


</style>
