<template>
  <v-row justify="center">
    <v-dialog
      :value="event"
      v-model="isOpen"
      @click:outside="close"
      width="540px"
    >
      <v-card class="px-5">
        <v-form :disabled="!formEnabled">
          <v-card-title
            v-text="event.activityName"
            class="py-8 justify-center"
          />
          <validation-observer v-slot="{ invalid }" slim>
            <v-card-text>
              <validation-provider
                v-slot="{ errors }"
                rules="required"
                name="eventDate"
              >
                <v-text-field
                  :value="event.schoolGroupName"
                  :label="$t('groups.parentGroup')"
                  :readonly="true"
                  :disabled="true"
                />
                <v-text-field
                  :value="group.instructorName"
                  :label="$t('general.instructor')"
                  :readonly="true"
                  :disabled="true"
                />

                <date-input
                  v-model="eventDate"
                  text-field-classes="mb-3"
                  :label="$t('time.eventDate')"
                  :error-messages="errors"
                />
              </validation-provider>
              <validation-provider
                v-slot="{ errors }"
                rules="required"
                name="startTime"
              >
                <time-input
                  v-model="startTime"
                  text-field-classes="mb-3"
                  :label="$t('time.eventStartTime')"
                  :error-messages="errors"
                />
              </validation-provider>
              <validation-provider
                v-slot="{ errors }"
                rules="required|afterStartTime:@startTime"
              >
                <time-input
                  v-model="endTime"
                  text-field-classes="mb-3"
                  :label="$t('time.eventEndTime')"
                  :error-messages="errors"
                />
              </validation-provider>
              <validation-provider v-slot="{ errors }" rules="required">
                <v-text-field
                  v-model="event.locationsName"
                  class="mb-3"
                  :label="$t('myActivity.location')"
                  append-icon="mdi-map-marker"
                  :error-messages="errors"
                />
              </validation-provider>
            </v-card-text>
            <v-card-actions>
              <v-btn
                v-if="!formEnabled"
                class="mt-4"
                color="primary"
                v-text="$tc('userActions.edit', 2)"
                @click="formEnabled = true"
              />

              <v-btn
                v-if="formEnabled"
                class="mt-4"
                color="primary"
                v-text="$t('userActions.save')"
                :disabled="invalid"
                @click="saveEvent"
              />
              <v-btn
                class="mt-4 mx-4"
                color="primary"
                outlined
                v-text="$t('userActions.cancel')"
                @click="close"
              />
              <v-btn
                class="mt-4 mx-4 absolute-left"
                color="error"
                outlined
                @click="showApproveDeleteDialog = true"
              >
                {{ $t("userActions.delete") }}
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-card-actions>
          </validation-observer>
          <modal-approve
            v-model="showApproveDeleteDialog"
            @approve="deleteEvent"
          >
            {{ this.$t("confirm.AreYouSureYouWantToDelete?") }}
          </modal-approve>
        </v-form>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import moment from "moment"
import { ValidationObserver, ValidationProvider } from "vee-validate"
import Api from "@/api"
import Utils from "@/helpers/utils"
import DateInput from "@/components/DateInput"
import TimeInput from "@/components/TimeInput"
import ModalApprove from "@/components/ModalApprove"

export default {
  created() {
    this.eventDate = moment(this.event.startTime).format("YYYY-MM-DD")
    this.startTime = moment(this.event.startTime).format("HH:mm")
    this.endTime = moment(this.event.endTime).format("HH:mm")
    this.originalStartDate = this.eventDate
  },
  components: {
    DateInput,
    TimeInput,
    ValidationObserver,
    ValidationProvider,
    ModalApprove,
  },
  props: {
    event: {
      type: Object,
      required: true,
    },
    group: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      formEnabled: false,
      eventDate: "2000-01-01",
      startTime: "10:00",
      endTime: "11:00",
      isOpen: true,
      originalStartDate: "2000-01-01",
      showApproveDeleteDialog: false,
    }
  },
  methods: {
    close() {
      this.$emit("close", false)
    },
    async saveEvent() {
      const startTime = Utils.dateToApiString(
        moment(`${this.eventDate}T${this.startTime}`)
      )
      const endTime = Utils.dateToApiString(
        moment(`${this.eventDate}T${this.endTime}`)
      )
      // TODO - this is not working yet:
      const now = Date.now()
      if (this.originalStartDate < now || startTime < now) {
        throw "Cannot update event in the past, or move it to the past"
      }
      const data = {
        startTime: startTime,
        endTime: endTime,
        locationsName: this.event.locationsName,
      }
      await Api.instructorEvent.updateEvent(this.event.slug, data)
      this.$emit("eventUpdated", this.originalStartDate)
      this.close()
    },
    async deleteEvent() {
      this.showApproveDeleteDialog = false
      await Api.event.deleteEvent(this.event.slug)
      this.$emit("eventUpdated", this.originalStartDate)
      this.close()
    },
  },
}
</script>
