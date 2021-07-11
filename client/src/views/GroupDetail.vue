<template>
  <div class="pt-8 pa-lg-16">
    <v-row class="mx-0">
      <v-col cols="12" lg="7">
        <div class="d-sm-flex justify-space-between mb-10">
          <div>
            <h1 v-text="$t('groups.groupPage')" class="mb-5" />
            <h2 v-text="$t('groups.editAndViewTheGroupDetails')" class="" />
          </div>
          <v-btn
            tile
            large
            color="error"
            class="mx-auto mx-sm-0 d-block my-10 my-sm-0"
            @click="isModalOpen = true"
          >
            {{ $t("userActions.delete") }}
            <v-icon right> mdi-close </v-icon>
          </v-btn>
        </div>

        <validation-observer
          tag="form"
          v-slot="{ invalid }"
          @submit.prevent="onSubmit"
        >
          <input-drawer
            unique-name="name"
            :label="$t('groups.groupName')"
            rules="required"
            v-model="name"
          />
          <input-drawer
            unique-name="description"
            :label="$t('general.description')"
            rules="required"
            v-model="description"
          />
          <v-btn
            class="my-16 py-5 white--text"
            type="submit"
            color="primary"
            elevation="3"
            v-text="$t('userActions.save')"
            :disabled="invalid"
          />
          <v-btn
            class="my-16 mx-2 mx-lg-8 py-5 white--text"
            elevation="3"
            type="button"
            color="primary"
            outlined
            v-text="$t('groups.viewAndEditStudents')"
            @click="
              $router.push({
                name: 'AssignGroupConsumers',
                params: { groupSlug },
              })
            "
          />
        </validation-observer>
      </v-col>
      <v-col cols="12" lg="5">
        <sticky-note>
          {{ this.$t("groups.thisGroupIsUnderProgram") }}
          "{{ this.programName }}"
        </sticky-note>
        <sticky-note class="mt-14">
          {{ this.$t("groups.numberOfStudentsSignedInToThisGroup") }}:
          {{ this.consumersNumber }}
        </sticky-note>
      </v-col>
    </v-row>
    <modal-approve v-model="isModalOpen" @approve="handleDelete">
      {{ this.$t("confirm.AreYouSureYouWantToDeleteThisGroup?") }}
    </modal-approve>
  </div>
</template>

<script>
import { ValidationObserver } from "vee-validate"
import { mapActions } from "vuex"
import Api from "../api"
import store from "../vuex/store"
import inputDrawer from "../components/InputDrawer"
import StickyNote from "../components/StickyNote"
import ModalApprove from "../components/ModalApprove"

export default {
  components: { ValidationObserver, inputDrawer, StickyNote, ModalApprove },
  async beforeRouteEnter(to, from, next) {
    const group = await store.dispatch(
      "programGroup/getGroup",
      to.params.groupSlug
    )
    next(vm => {
      vm.name = group.name
      vm.description = group.description
      vm.programName = group.activityName
      vm.consumersNumber = group.consumers.length
    })
  },
  props: {
    groupSlug: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      isModalOpen: false,
      name: "",
      description: "",
      programName: "",
      consumersNumber: 0,
    }
  },
  methods: {
    ...mapActions("programGroup", ["updateGroup", "deleteGroup"]),
    ...mapActions("snackbar", ["showMessage"]),
    async onSubmit() {
      try {
        await this.updateGroup({
          groupSlug: this.groupSlug,
          data: {
            name: this.name,
            description: this.description,
          },
        })
        this.showMessage(this.$t("general.detailsSuccessfullyUpdated"))
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },
    async handleDelete() {
      try {
        await this.deleteGroup(this.groupSlug)
        this.showMessage(this.$t("groups.groupDeletedSuccessfully"))
        this.$router.push({ name: "MyGroups" })
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },
  },
}
</script>
