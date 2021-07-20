<template>
  <div class="wrapper">
    <v-card
      class="py-12 px-7 mx-auto"
      width="320"
      elevation="16"
      v-show="page === 1"
    >
      <v-card-title class="text-h4 justify-center mb-6">{{
        $t("auth.detailsCompletion")
      }}</v-card-title>
      <v-card-subtitle class="text-h6 text-center mb-8">{{
        $t("general.personalInfo")
      }}</v-card-subtitle>
      <validation-observer ref="observer" v-slot="{ invalid }">
        <form @submit.prevent="incrementPage" data-testid="form-1">
          <validation-provider v-slot="{ errors }" name="name" rules="required">
            <v-text-field
              v-model="registrationInfo.name"
              data-testid="name"
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
              v-model="registrationInfo.phone"
              data-testid="phone"
              :error-messages="errors"
              :label="$t('general.phoneNumber')"
              required
            />
          </validation-provider>

          <div class="mx-auto d-flex justify-center mt-12">
            <v-btn
              class="ml-3 white--text"
              type="submit"
              color="primary"
              elevation="3"
              :disabled="invalid"
            >
              {{ $t("userActions.next") }}
            </v-btn>
            <v-btn
              class="mr-3"
              type="button"
              color="primary"
              elevation="3"
              outlined
              @click="logout"
            >
              {{ $t("userActions.toHomepage") }}
            </v-btn>
          </div>
        </form>
      </validation-observer>
    </v-card>
    <v-card
      v-if="shouldEditSchool"
      v-show="page === 2"
      class="py-12 px-7 mx-auto"
      width="320"
      elevation="16"
    >
      <v-card-title class="text-h4 justify-center mb-6">{{
        $t("auth.detailsCompletion")
      }}</v-card-title>
      <v-card-subtitle class="text-h6 text-center mb-6">{{
        $t("general.schoolDetails")
      }}</v-card-subtitle>
      <validation-observer ref="observer" v-slot="{ invalid }">
        <form @submit.prevent="incrementPage" data-testid="form-2">
          <validation-provider
            v-slot="{ errors }"
            name="school"
            rules="required"
          >
            <v-text-field
              data-testid="school"
              v-model="registrationInfo.schoolName"
              :error-messages="errors"
              :label="$t('general.schoolName')"
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="schoolCode"
            rules="required|numeric"
          >
            <v-text-field
              data-testid="school-code"
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
              data-testid="school-city"
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
              data-testid="street"
              v-model="registrationInfo.schoolStreet"
              :error-messages="errors"
              :label="$t('general.street')"
              required
            ></v-text-field>
          </validation-provider>

          <validation-provider
            v-slot="{ errors }"
            name="schoolPhone"
            rules="required|numeric|phoneNumberIsrael"
          >
            <v-text-field
              data-testid="school-phone"
              v-model="registrationInfo.schoolPhone"
              :error-messages="errors"
              :label="$t('general.schoolPhoneNumber')"
              required
            ></v-text-field>
          </validation-provider>

          <validation-provider
            v-slot="{ errors }"
            name="schoolGrades"
            rules="required"
          >
            <v-select
              data-testid="school-grades"
              v-model="registrationInfo.schoolGrades"
              :error-messages="errors"
              :items="SCHOOL_GRADES_ITEMS"
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
              color="primary"
              elevation="3"
              :disabled="invalid"
            >
              {{ $t("userActions.next") }}
            </v-btn>
            <v-btn
              class="mr-3"
              type="button"
              color="primary"
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
    <v-card
      class="py-12 px-7 mx-auto"
      width="320"
      elevation="16"
      v-show="
        (page === 3 && shouldEditSchool) || (page === 2 && !shouldEditSchool)
      "
    >
      <v-card-title class="text-h4 justify-center mb-6">{{
        $t("auth.detailsCompletion")
      }}</v-card-title>
      <v-card-subtitle class="text-h6 text-center mb-8">{{
        $t("auth.confirmDetails")
      }}</v-card-subtitle>
      <form @submit.prevent="submit" data-testid="form-3">
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
        <template v-if="shouldEditSchool">
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
            ><b>{{ $t("general.phoneNumber") }}:</b>
            {{ registrationInfo.schoolPhone }}</v-card-text
          >
          <v-card-text
            ><b>{{ $t("general.schoolGrades") }}:</b>
            {{
              registrationInfo.schoolGrades
                .map(num => $t(`grades.${num}`))
                .join(", ")
            }}</v-card-text
          >
        </template>

        <div class="mx-auto d-flex justify-center mt-12">
          <v-btn
            class="ml-3 white--text"
            type="submit"
            color="primary"
            elevation="3"
          >
            {{ $t("auth.detailsConfirmation") }}
          </v-btn>
          <v-btn
            class="mr-3"
            type="button"
            color="primary"
            elevation="3"
            outlined
            @click="decrementPage()"
          >
            {{ $t("userActions.back") }}
          </v-btn>
        </div>
      </form>
    </v-card>
    <modal
      :redirectComponentName="modalRedirectComponentName"
      v-show="popupMsg !== ''"
      @close="popupMsg = ''"
    >
      {{ popupMsg }}
    </modal>
  </div>
</template>
<script>
import store from "../../vuex/store"
import debounce from "lodash/debounce"
import { mapActions } from "vuex"
import { ValidationObserver, ValidationProvider } from "vee-validate"
import { SCHOOL_GRADES_ITEMS } from "../../helpers/constants/constants"
import Modal from "../../components/Modal"

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    Modal,
  },
  props: {
    shouldEditSchool: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      SCHOOL_GRADES_ITEMS,
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
        schoolPhone: "",
        schoolGrades: [],
      },
    }
  },

  async mounted() {
    let userDetails = await store.dispatch("user/getUserDetails")
    let schoolDetails = await store.dispatch("school/getSchoolDetails")
    this.slug = userDetails.slug
    this.schoolSlug = schoolDetails.slug
  },

  methods: {
    ...mapActions("user", ["updateUserDetails"]),
    ...mapActions("coordinator", ["updateProfile"]),
    ...mapActions("school", ["updateSchoolDetails"]),
    ...mapActions("auth", ["logout"]),
    submit: debounce(
      function () {
        let userDetailsPayload = this.createUserSubmitPayload()
        let profilePayload = this.createProfileSubmitPayload()
        let schoolPayload = this.createSchoolSubmitPayload()
        this.postRegistrationData(
          userDetailsPayload,
          profilePayload,
          schoolPayload
        )
      },
      500,
      { leading: true, trailing: false }
    ),

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
      let data = new FormData()
      data.append("slug", this.schoolSlug)
      data.append("name", this.registrationInfo.schoolName)
      data.append("address", this.registrationInfo.schoolStreet)
      data.append("address_city", this.registrationInfo.schoolCity)
      data.append("school_code", this.registrationInfo.schoolCode)
      data.append("contact_phone", this.registrationInfo.schoolPhone)
      data.append(
        "grade_levels",
        JSON.stringify(this.registrationInfo.schoolGrades)
      )
      return data
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
        if (this.shouldEditSchool) {
          await this.updateSchoolDetails({
            slug: this.schoolSlug,
            schoolDetails: schoolPayload,
          })
        }
        this.modalRedirectComponentName = "MyGroups"
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
.wrapper {
  margin-top: 100px;
  margin-bottom: 30px;
}

.v-card__subtitle,
.v-card__text,
.v-card__title {
  padding: 0;
}
</style>
