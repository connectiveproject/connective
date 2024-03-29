<template>
  <div class="w-75 mx-auto">
    <div class="d-flex justify-space-between py-10 flex-wrap">
      <div>
        <h1 class="pb-4" v-text="$t('events.requestsForEvents')" />
        <h2
          v-text="$t('events.approveOrDenyEventsRequestsFromSchoolGroups')"
          class="pb-12"
        />
      </div>
      <v-btn
        tile
        large
        :class="{ 'd-block mx-auto': $vuetify.breakpoint.xs }"
        color="success"
        @click="$router.push({ name: 'CoordinatorEventCreator' })"
      >
        {{ $t("events.newEvent") }}
        <v-icon right> mdi-plus </v-icon>
      </v-btn>
    </div>
    <pagination-actions-table
      class="mb-16"
      disable-sort
      :loading="loading"
      :headers="headers"
      :items="readableEventOrders"
      :total-actions="1"
      :actions-title="$t('userActions.delete')"
      :action-one-icon-tooltip="$t('userActions.delete')"
      action-one-icon="mdi-delete"
      action-one-icon-color="red darken-1"
      @action-one-click="onDeleteClick"
      @paginate="getOrders"
    />
    <modal-approve v-model="isModalOpen" @approve="deleteOrder">
      {{
        this.$t(
          "confirm.AreYouSureYouWantToDeleteThisOrder?ThisActionWillDeleteAllRelatedEvents"
        )
      }}
    </modal-approve>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "@/vuex/store"
import Api from "../api"
import Utils from "../helpers/utils"
import { SERVER } from "../helpers/constants/constants"
import PaginationActionsTable from "../components/Tables/PaginationActionsTable"
import ModalApprove from "../components/ModalApprove"

export default {
  components: { PaginationActionsTable, ModalApprove },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("event/getEventOrders", {
      override: true,
      userPagination: true,
    })
    next()
  },
  computed: {
    ...mapState("event", ["eventOrders"]),
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
      orderToDelete: null,
      isModalOpen: false,
      headers: [
        {
          text: this.$t("groups.groupName"),
          value: "schoolGroupName",
        },
        {
          text: this.$t("general.schoolName"),
          value: "schoolName",
        },
        {
          text: this.$t("program.programName"),
          value: "activityName",
        },
        {
          text: this.$t("myActivity.location"),
          value: "locationsName",
        },
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
    ...mapActions("event", ["deleteEventOrder", "getEventOrders"]),
    ...mapActions("snackbar", ["showMessage"]),
    async getOrders() {
      this.loading = true
      await this.getEventOrders({ override: true, usePagination: true })
      this.loading = false
    },
    onDeleteClick: debounce(
      function (order) {
        this.orderToDelete = order
        this.isModalOpen = true
      },
      500,
      { leading: true, trailing: false }
    ),

    async deleteOrder() {
      try {
        await this.deleteEventOrder(this.orderToDelete.slug)
        this.showMessage(
          this.$t("success.eventOrderAndEventsSuccessfullyDeleted")
        )
        this.getOrders()
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },
  },
}
</script>
