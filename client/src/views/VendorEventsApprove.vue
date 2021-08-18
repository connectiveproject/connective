<template>
  <div>
    <h1 class="pb-4" v-text="$t('events.requestsForEvents')" />
    <h2
      v-text="$t('events.approveOrDenyEventsRequestsFromSchoolGroups')"
      class="pb-12"
    />
    <pagination-actions-table
      introjs="actions-table"
      disable-sort
      class="mb-10"
      :loading="loading"
      :headers="headers"
      :items="readableEventOrders"
      :actions-title="$t('userActions.denyOrApprove')"
      :action-two-icon-tooltip="`${$t('userActions.deny')} / ${$t(
        'userActions.cancel'
      )}`"
      @action-one-click="onApproveClick"
      @action-two-click="onRejectClick"
      @paginate="getOrders"
    />
    <modal-approve v-model="isModalOpen" @approve="approveOrder">
      {{
        this.$t(
          "confirm.AreYouSureYouWantToApproveThisRequest?ThisActionWillAddTheEventsToTheGroupSchedule"
        )
      }}
    </modal-approve>
    <form-dialog
      v-model="isDenyFormDialogActive"
      :title="$tc('general.additionalInfo', 0)"
      :subtitle="`${$t(
        'events.attention!ThisActionWillDeleteAllRelatedEvents'
      )}.`"
      :input-fields="rejectDialogFields"
      @save="rejectOrder"
    />
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "../vuex/store"
import Api from "../api"
import Utils from "../helpers/utils"
import { SERVER } from "../helpers/constants/constants"
import PaginationActionsTable from "../components/Tables/PaginationActionsTable"
import ModalApprove from "../components/ModalApprove"
import FormDialog from "../components/FormDialog"
import introjsSubscribeMixin from "../mixins/introJs/introjsSubscribeMixin"

export default {
  name: "VendorEventsApprove",
  components: { PaginationActionsTable, ModalApprove, FormDialog },
  mixins: [introjsSubscribeMixin],
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("vendorEvent/getEventOrders", {
      override: true,
      usePagination: true,
    })
    next()
  },
  computed: {
    ...mapState("vendorEvent", ["eventOrders"]),
    readableEventOrders() {
      return this.eventOrders.map(order => {
        const readableStartTime = Utils.ApiStringToReadableDate(order.startTime)
        const readableEndTime = Utils.ApiStringToReadableDate(order.endTime)
        const readableStatus = this.$t(
          `status.${Object.keys(SERVER.eventOrderStatus).find(
            key => SERVER.eventOrderStatus[key] === order.status
          )}`
        )
        const readableRecurrence = this.$t(
          `time.${Object.keys(SERVER.eventOrderReccurence).find(
            key => SERVER.eventOrderReccurence[key] === order.recurrence
          )}`
        )
        return {
          ...order,
          readableStartTime,
          readableEndTime,
          readableStatus,
          readableRecurrence,
        }
      })
    },
  },
  data() {
    return {
      loading: false,
      orderToApprove: null,
      orderToReject: null,
      isModalOpen: false,
      isDenyFormDialogActive: false,
      rejectDialogFields: [
        {
          name: "statusReason",
          rule: "required",
          label: this.$t("events.reasonForEventsDenyOrCancellation"),
          value: "",
        },
      ],
      headers: [
        { text: this.$t("groups.groupName"), value: "schoolGroupName" },
        { text: this.$t("general.schoolName"), value: "schoolName" },
        { text: this.$t("program.programName"), value: "activityName" },
        { text: this.$t("myActivity.location"), value: "locationsName" },
        {
          text: this.$t("time.startDate"),
          value: "readableStartTime",
        },
        {
          text: this.$t("time.endDate"),
          value: "readableEndTime",
        },
        {
          text: this.$t("time.recurrence"),
          value: "readableRecurrence",
        },
        {
          text: this.$t("general.status"),
          value: "readableStatus",
        },
        {
          text: this.$t("events.reasonForDenyOrCancellation"),
          value: "statusReason",
        },
      ],
    }
  },
  methods: {
    ...mapActions("vendorEvent", ["updateEventOrder", "getEventOrders"]),
    ...mapActions("snackbar", ["showMessage"]),
    async getOrders() {
      this.loading = true
      await this.getEventOrders({ override: true, usePagination: true })
      this.loading = false
    },
    onApproveClick: debounce(
      async function (order) {
        if (order.status !== SERVER.eventOrderStatus.pendingVendorApproval) {
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

    onRejectClick: debounce(
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
        this.orderToReject = order
        this.isDenyFormDialogActive = true
      },
      500,
      {
        leading: true,
        trailing: false,
      }
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

    rejectOrder({ statusReason }) {
      if (this.orderToReject.status === SERVER.eventOrderStatus.approved) {
        return this.cancelOrder({ ...this.orderToReject, statusReason })
      }
      if (
        this.orderToReject.status ===
        SERVER.eventOrderStatus.pendingVendorApproval
      ) {
        return this.denyOrder({ ...this.orderToReject, statusReason })
      }
    },

    async cancelOrder(order) {
      try {
        await this.updateEventOrder({
          slug: order.slug,
          data: {
            status: SERVER.eventOrderStatus.cancelled,
            statusReason: order.statusReason,
          },
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
          data: {
            status: SERVER.eventOrderStatus.denied,
            statusReason: order.statusReason,
          },
        })
        this.showMessage(this.$t("success.eventDenied"))
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },
  },
}
</script>
