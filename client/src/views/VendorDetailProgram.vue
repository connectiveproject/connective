<template>
  <div>
    <validation-observer
      tag="form"
      v-slot="{ invalid }"
      @submit.prevent="onSubmit"
      v-if="program"
    >
      <v-row no-gutters>
        <v-col cols="12" lg="7" class="mb-12 mb-lg-0">
          <div class="d-sm-flex justify-space-between mb-10">
            <div>
              <h1 v-text="$t('program.programPage')" class="mb-5" />
              <h2 v-text="$t('program.editAndViewTheProgramDetails')" />
            </div>
            <v-btn
              tile
              large
              color="error"
              class="mx-auto mx-sm-0 d-block my-10 my-sm-0"
              data-testid="delete-btn"
              @click="isModalOpen = true"
            >
              {{ $t("userActions.delete") }}
              <v-icon right> mdi-close </v-icon>
            </v-btn>
          </div>

          <input-drawer
            v-for="field in programFields"
            v-model="program[field.name]"
            :key="field.id"
            :unique-name="field.name"
            :label="field.label"
            :rules="field.rules"
            :type="field.type || 'text'"
            :choices="field.choices"
            :multiselect="field.multiselect"
            :valueData.sync="program[field.name]"
          />
        </v-col>
        <v-col cols="12" lg="5" class="px-10" align-self="center">
          <picture-input
            class="mx-auto"
            v-model="logo"
            :placeholderPicUrl="program.logo || CAMERA_ROUNDED_DRAWING"
          />
        </v-col>
      </v-row>
      <div class="mx-auto mx-md-0 my-16">
        <v-btn
          class="mx-2 white--text"
          type="submit"
          color="primary"
          elevation="3"
          :disabled="invalid"
          :loading="loading"
        >
          {{ $t("userActions.save") }}
        </v-btn>
        <v-btn
          class="mx-2 white--text"
          elevation="3"
          type="button"
          color="primary"
          outlined
          @click="
            $router.push({
              name: 'VendorProgramMediaUpload',
              params: { programSlug },
            })
          "
        >
          {{ $t("userActions.addMedia") }}
          <v-icon right> mdi-plus </v-icon>
        </v-btn>
      </div>
    </validation-observer>

    <modal-approve v-model="isModalOpen" @approve="handleDelete">
      {{ this.$t("confirm.AreYouSureYouWantToDeleteThisProgram?") }}
    </modal-approve>
  </div>
</template>

<script>
import { ValidationObserver } from "vee-validate"
import { mapActions } from "vuex"
import Utils from "@/helpers/utils"
import Api from "@/api"
import store from "@/vuex/store"
import { CAMERA_ROUNDED_DRAWING } from "@/helpers/constants/images"
import inputDrawer from "@/components/InputDrawer"
import ModalApprove from "@/components/ModalApprove"
import PictureInput from "@/components/PictureInput"

export default {
  components: {
    ValidationObserver,
    inputDrawer,
    ModalApprove,
    PictureInput,
  },
  async beforeRouteEnter(to, from, next) {
    const program = await store.dispatch(
      "vendorProgram/getProgram",
      to.params.programSlug
    )
    next(vm => (vm.program = program))
  },
  props: {
    programSlug: {
      type: String,
      required: true,
    },
  },
  data() {
    const vendorProgramFields = Utils.getVendorProgramFields()
    return {
      CAMERA_ROUNDED_DRAWING,
      programFields: vendorProgramFields.filter(field => field.name !== "logo"),
      isModalOpen: false,
      program: null,
      logo: null,
      loading: false,
    }
  },
  methods: {
    ...mapActions("vendorProgram", ["updateProgram", "deleteProgram"]),
    ...mapActions("snackbar", ["showMessage"]),
    async onSubmit() {
      try {
        this.loading = true
        const activityWebsiteUrl = Utils.addWebsiteScheme(
          this.program.activityWebsiteUrl
        )
        const data = Utils.objectToFormData({
          ...this.program,
          activityWebsiteUrl,
        })
        data.delete("logo")
        if (this.logo) {
          data.set("logo", this.logo)
        }
        await this.updateProgram({
          programSlug: this.programSlug,
          data,
        })
        this.showMessage(this.$t("general.detailsSuccessfullyUpdated"))
        this.$router.push({ name: "VendorProgramList" })
        this.loading = false
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
        this.loading = false
      }
    },
    async handleDelete() {
      try {
        await this.deleteProgram(this.programSlug)
        this.showMessage(this.$t("success.programDeletedSuccessfully"))
        this.$router.push({ name: "VendorProgramList" })
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },
  },
}
</script>
