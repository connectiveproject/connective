<template>
  <div>
    <actions-table
      :headers="headers"
      :items="eventOrders"
      :action-two-icon-tooltip="`${$t('userActions.deny')} / ${$t(
        'userActions.cancel'
      )}`"
      @action-one-click="onApproveClick"
      @action-two-click="rejectOrder"
    />
    <modal-approve v-model="isModalOpen" @approve="approveOrder">
      {{
        this.$t(
          "confirm.AreYouSureYouWantToApproveThisRequest?ThisActionWillStartCollaborationWithTheSchoolAndCreateTheRelevantEvents"
        )
      }}
    </modal-approve>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "../vuex/store"
import Api from "../api"
import { SERVER } from "../helpers/constants/constants"
import ActionsTable from "../components/ActionsTable"
import ModalApprove from "../components/ModalApprove"

export default {
  components: { ActionsTable, ModalApprove },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("vendorEvent/getEventOrders")
    next()
  },
  computed: {
    ...mapState("vendorEvent", ["eventOrders"]),
  },
  data() {
    return {
      orderToApprove: null,
      isModalOpen: false,
      headers: [
        { text: this.$t("groups.groupName"), value: "schoolGroupName" },
        { text: this.$t("general.schoolName"), value: "schoolName" },
        { text: this.$t("program.programName"), value: "activityName" },
        { text: this.$t("myActivity.location"), value: "locationsName" },
        { text: this.$t("time.startTime"), value: "startTime" },
        { text: this.$t("time.endTime"), value: "endTime" },
        { text: this.$t("time.recurrence"), value: "recurrence" },
        { text: this.$t("general.status"), value: "status" },
      ],
    }
  },
  methods: {
    ...mapActions("vendorEvent", ["updateEventOrder"]),
    ...mapActions("snackbar", ["showMessage"]),
    onApproveClick: debounce(
      async function (order) {
        if (order.status !== SERVER.eventOrderStatus.pendingApproval) {
          return this.showMessage(
            this.$t("errors.cantApproveEventsThatArentPendingApproval")
          )
        }
        this.orderToApprove = order
        this.isModalOpen = true
      },
      500,
      { leading: true, trailing: false }
    ),

    async approveOrder() {
      try {
        await this.updateEventOrder({
          slug: this.orderToApprove.slug,
          data: { status: SERVER.eventOrderStatus.approved },
        })
        this.showMessage(this.$t("success.eventSuccessfullyApproved"))
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },

    rejectOrder: debounce(
      async function (order) {
        if (
          [
            SERVER.eventOrderStatus.cancelled,
            SERVER.eventOrderStatus.cancelled,
          ].includes(order.status)
        ) {
          return this.showMessage(
            this.$t("errors.cantRejectAlreadyCancelledOrDeniedEvents")
          )
        }
        if (order.status === SERVER.eventOrderStatus.approved) {
          return this.cancelOrder(order)
        }
        if (order.status === SERVER.eventOrderStatus.pendingApproval) {
          return this.denyOrder(order)
        }
      },
      500,
      {
        leading: true,
        trailing: false,
      }
    ),

    async cancelOrder(order) {
      try {
        await this.updateEventOrder({
          slug: order.slug,
          data: { status: SERVER.eventOrderStatus.cancelled },
        })
        this.showMessage(this.$t("success.allRelatedEventsHaveBeenCancelled"))
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },

    async denyOrder(order) {
      try {
        await this.updateEventOrder({
          slug: order.slug,
          data: { status: SERVER.eventOrderStatus.denied },
        })
        this.showMessage(this.$t("success.eventDenied"))
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },
  },
}
</script>
