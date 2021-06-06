<template>
  <v-container>
    <v-row dense justify="center">
      <v-col cols="11" sm="6" md="6" lg="4" xl="3" v-show="page === 1">
        <v-card
          class="mx-auto py-12 px-5 registration-card"
          elevation="20"
          outlined
        >
          <v-card-title
            class="purple--text text--darken-4 text-h4 justify-center mb-6"
            >{{ $t("auth.detailsCompletion") }}</v-card-title
          >
          <v-card-subtitle
            class="purple--text text--darken-4 text-h6 text-center mb-8"
            >{{ $t("general.personalInfo") }}</v-card-subtitle
          >
          <validation-observer ref="observer" v-slot="{ invalid }">
            <form @submit.prevent="incrementPage">
              <validation-provider
                v-slot="{ errors }"
                name="name"
                rules="required"
              >
                <v-text-field
                  class="mt-5"
                  v-model="registrationInfo.name"
                  :error-messages="errors"
                  :label="$t('general.name')"
                  required
                ></v-text-field>
              </validation-provider>

              <validation-provider
                v-slot="{ errors }"
                name="phone"
                rules="required|numeric|phoneNumberIsrael"
              >
                <v-text-field
                  class="mt-5"
                  v-model="registrationInfo.phone"
                  :error-messages="errors"
                  :label="$t('general.phoneNumber')"
                  required
                />
              </validation-provider>

              <div class="mx-auto d-flex justify-center mt-12">
                <v-btn
                  class="ml-3 white--text"
                  type="submit"
                  color="purple darken-3"
                  elevation="3"
                  :disabled="invalid"
                >
                  {{ $t("userActions.next") }}
                </v-btn>
              </div>
            </form>
          </validation-observer>
        </v-card>
      </v-col>

      <v-col cols="11" sm="6" md="6" lg="4" xl="3" v-show="page === 2">
        <v-card
          class="mx-auto py-12 px-5 registration-card"
          elevation="20"
          outlined
        >
          <v-card-title
            class="purple--text text--darken-4 text-h4 justify-center mb-6"
            >{{ $t("auth.detailsCompletion") }}</v-card-title
          >
          <v-card-subtitle
            class="purple--text text--darken-4 text-h6 text-center mb-6"
            >{{ $t("general.schoolDetails") }}</v-card-subtitle
          >
          <validation-observer ref="observer" v-slot="{ invalid }">
            <form @submit.prevent="incrementPage">
              <validation-provider
                v-slot="{ errors }"
                name="school"
                rules="required"
              >
                <v-text-field
                  class="mt-5"
                  v-model="registrationInfo.schoolName"
                  :error-messages="errors"
                  :label="$tc('general.school', 0)"
                  required
                ></v-text-field>
              </validation-provider>
              <validation-provider
                v-slot="{ errors }"
                name="schoolCode"
                rules="required|numeric"
              >
                <v-text-field
                  class="mt-5"
                  v-model="registrationInfo.schoolCode"
                  :error-messages="errors"
                  :label="$t('general.schoolCode')"
                  required
                ></v-text-field>
              </validation-provider>

              <validation-provider
                v-slot="{ errors }"
                name="schoolCity"
                rules="required"
              >
                <v-text-field
                  class="mt-5"
                  v-model="registrationInfo.schoolCity"
                  :error-messages="errors"
                  :label="$t('general.city')"
                  required
                ></v-text-field>
              </validation-provider>

              <validation-provider
                v-slot="{ errors }"
                name="schoolStreet"
                rules="required"
              >
                <v-text-field
                  class="mt-5"
                  v-model="registrationInfo.schoolStreet"
                  :error-messages="errors"
                  :label="$t('general.street')"
                  required
                ></v-text-field>
              </validation-provider>

              <validation-provider
                v-slot="{ errors }"
                name="schoolZipCode"
                :rules="zipCodeValidationRule"
              >
                <v-text-field
                  class="mt-5"
                  v-model="registrationInfo.schoolZipCode"
                  :error-messages="errors"
                  :label="$t('general.zipCode')"
                  required
                ></v-text-field>
              </validation-provider>

              <validation-provider
                v-slot="{ errors }"
                name="schoolPhone"
                rules="required|numeric|phoneNumberIsrael"
              >
                <v-text-field
                  class="mt-5"
                  v-model="registrationInfo.schoolPhone"
                  :error-messages="errors"
                  :label="$t('general.phoneNumber')"
                  required
                ></v-text-field>
              </validation-provider>

              <validation-provider
                v-slot="{ errors }"
                name="schoolDescription"
                rules="required"
              >
                <v-text-field
                  class="mt-5"
                  v-model="registrationInfo.schoolDescription"
                  :error-messages="errors"
                  :label="$t('general.description')"
                  required
                ></v-text-field>
              </validation-provider>

              <validation-provider
                v-slot="{ errors }"
                name="schoolWebsite"
                rules="required|website"
              >
                <v-text-field
                  class="mt-5"
                  v-model="registrationInfo.schoolWebsite"
                  :error-messages="errors"
                  :label="$t('general.website')"
                  required
                ></v-text-field>
              </validation-provider>

              <validation-provider
                v-slot="{ errors }"
                name="schoolGrades"
                rules="required"
              >
                <v-select
                  class="mt-5"
                  v-model="registrationInfo.schoolGrades"
                  :error-messages="errors"
                  :items="schoolGradesItems"
                  :label="$t('general.schoolGrades')"
                  multiple
                  chips
                  deletable-chips
                >
                </v-select>
              </validation-provider>

              <div class="mx-auto d-flex justify-center mt-12">
                <v-btn
                  class="ml-3 white--text"
                  type="submit"
                  color="purple darken-3"
                  elevation="3"
                  :disabled="invalid"
                >
                  {{ $t("userActions.next") }}
                </v-btn>
                <v-btn
                  class="mr-3"
                  type="button"
                  color="purple darken-3"
                  elevation="3"
                  outlined
                  @click="decrementPage()"
                >
                  {{ $t("userActions.back") }}
                </v-btn>
              </div>
            </form>
          </validation-observer>
        </v-card>
      </v-col>

      <v-col cols="11" sm="6" md="6" lg="4" xl="3" v-show="page === 3">
        <v-card
          class="mx-auto py-12 px-5 registration-card"
          elevation="20"
          outlined
        >
          <v-card-title
            class="purple--text text--darken-4 text-h4 justify-center mb-6"
            >{{ $t("auth.detailsCompletion") }}</v-card-title
          >
          <v-card-subtitle
            class="purple--text text--darken-4 text-h6 text-center mb-8"
            >{{ $t("auth.confirmDetails") }}</v-card-subtitle
          >
          <form @submit.prevent="submit">
            <v-card-text
              class="text-center mb-5 text-subtitle-1 font-weight-bold"
              >{{ $t("general.personalInfo") }}</v-card-text
            >
            <v-card-text
              ><b>{{ $t("general.name") }}:</b>
              {{ registrationInfo.name }}
            </v-card-text>
            <v-card-text
              ><b>{{ $t("general.phoneNumber") }}:</b>
              {{ registrationInfo.phone }}</v-card-text
            >
            <br />
            <v-card-text
              class="text-center mb-5 text-subtitle-1 font-weight-bold"
              >{{ $t("general.schoolDetails") }}</v-card-text
            >
            <v-card-text
              ><b>{{ $t("general.name") }} {{ $tc("general.school", 0) }}:</b>
              {{ registrationInfo.schoolName }}</v-card-text
            >
            <v-card-text
              ><b>{{ $t("general.schoolCode") }}:</b>
              {{ registrationInfo.schoolCode }}</v-card-text
            >
            <v-card-text
              ><b>{{ $t("general.city") }}:</b>
              {{ registrationInfo.schoolCity }}</v-card-text
            >
            <v-card-text
              ><b>{{ $t("general.street") }}:</b>
              {{ registrationInfo.schoolStreet }}</v-card-text
            >
            <v-card-text
              ><b>{{ $t("general.zipCode") }}:</b>
              {{ registrationInfo.schoolZipCode }}</v-card-text
            >
            <v-card-text
              ><b>{{ $t("general.phoneNumber") }}:</b>
              {{ registrationInfo.schoolPhone }}</v-card-text
            >
            <v-card-text
              ><b>{{ $t("general.description") }}:</b>
              {{ registrationInfo.schoolDescription }}</v-card-text
            >
            <v-card-text
              ><b>{{ $t("general.website") }}:</b>
              {{ registrationInfo.schoolWebsite }}</v-card-text
            >
            <v-card-text
              ><b>{{ $t("general.schoolGrades") }}:</b>
              {{ registrationInfo.schoolGrades }}</v-card-text
            >

            <div class="mx-auto d-flex justify-center mt-12">
              <v-btn
                class="ml-3 white--text"
                type="submit"
                color="purple darken-3"
                elevation="3"
              >
                {{ $t("auth.detailsCompletion") }}
              </v-btn>
              <v-btn
                class="mr-3"
                type="button"
                color="purple darken-3"
                elevation="3"
                outlined
                @click="decrementPage()"
              >
                {{ $t("userActions.back") }}
              </v-btn>
            </div>
          </form>
        </v-card>
      </v-col>
    </v-row>
    <modal
      :redirectComponentName="modalRedirectComponentName"
      v-show="popupMsg !== ''"
      @close="popupMsg = ''"
    >
      {{ popupMsg }}
    </modal>
  </v-container>
</template>
<script>
import store from "../vuex/store"
import { mapActions } from "vuex"
import { ValidationObserver, ValidationProvider } from "vee-validate"
import {
  schoolGradesItems,
  zipCodeValidationRule,
} from "../helpers/constants/constants"
import Modal from "../components/Modal"

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    Modal,
  },
  data: () => ({
    zipCodeValidationRule,
    schoolGradesItems,
    modalRedirectComponentName: "",
    slug: null,
    schoolSlug: "",
    showPass: false,
    page: 1,
    popupMsg: "",
    registrationInfo: {
      name: "",
      phone: "",
      schoolName: "",
      schoolCode: "",
      schoolCity: "",
      schoolStreet: "",
      schoolZipCode: "",
      schoolPhone: "",
      schoolDescription: "",
      schoolWebsite: "",
      schoolGrades: [],
    },
  }),

  mounted: async function () {
    let userDetails = await store.dispatch("user/getUserDetails")
    this.slug = userDetails.slug
    let schoolDetails = await store.dispatch("school/getSchoolDetails")
    this.schoolSlug = schoolDetails.slug
  },

  methods: {
    ...mapActions("user", ["updateUserDetails"]),
    ...mapActions("coordinator", ["updateProfile"]),
    ...mapActions("school", ["updateSchoolDetails"]),
    submit() {
      let userDetailsPayload = this.createUserSubmitPayload()
      let profilePayload = this.createProfileSubmitPayload()
      let schoolPayload = this.createSchoolSubmitPayload()
      this.postRegistrationData(
        userDetailsPayload,
        profilePayload,
        schoolPayload
      )
    },

    createUserSubmitPayload() {
      return {
        name: this.registrationInfo.name,
      }
    },

    createProfileSubmitPayload() {
      let profilePayload = new FormData()
      profilePayload.append("phone_number", this.registrationInfo.phone)
      return profilePayload
    },

    createSchoolSubmitPayload() {
      let payload = new FormData()
      payload.append("slug", this.schoolSlug)
      payload.append("name", this.registrationInfo.schoolName)
      payload.append("address", this.registrationInfo.schoolStreet)
      payload.append("address_city", this.registrationInfo.schoolCity)
      payload.append("zip_city", this.registrationInfo.schoolZipCode)
      payload.append("school_code", this.registrationInfo.schoolCode)
      payload.append("description", this.registrationInfo.schoolDescription)
      payload.append("contact_phone", this.registrationInfo.schoolPhone)
      payload.append("website", this.registrationInfo.schoolWebsite)
      payload.append(
        "grade_levels",
        JSON.stringify(this.registrationInfo.schoolGrades)
      )
      return payload
    },

    async postRegistrationData(
      userDetailsPayload,
      profilePayload,
      schoolPayload
    ) {
      try {
        await this.updateProfile({ slug: this.slug, profile: profilePayload })
        await this.updateUserDetails({
          slug: this.slug,
          userDetails: userDetailsPayload,
        })
        await this.updateSchoolDetails({
          slug: this.schoolSlug,
          schoolDetails: schoolPayload,
        })
        this.modalRedirectComponentName = "Profile"
        this.popupMsg = this.$t("general.detailsSuccessfullyUpdated")
      } catch (err) {
        if (
          err.response &&
          err.response.status === 400 &&
          Object.keys(err.response.data).length > 0
        ) {
          this.popupMsg =
            err.response.data[Object.keys(err.response.data)[0]][0]
        } else {
          this.popupMsg = this.$t("errors.genericError")
        }
      }
    },

    incrementPage() {
      this.page += 1
    },

    decrementPage() {
      this.page -= 1
    },
  },
}
</script>

<style lang="scss" scoped>
.registration-card {
  margin-top: 60px;
}

.v-card__subtitle,
.v-card__text,
.v-card__title {
  padding: 0;
}
</style>
