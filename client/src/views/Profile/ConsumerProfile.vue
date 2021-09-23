<template>
  <v-card
    class="wrapper mt-15 mx-auto px-5 px-sm-10 py-10"
    :elevation="$vuetify.breakpoint.xs ? 0 : 3"
    v-if="userAttributes"
  >
    <h1 class="mb-10">{{ $t("general.myProfile") }}</h1>
    <title-to-text
      v-for="(attrValue, attrName) in userAttributes"
      :key="attrName"
      :title="$t(`general.${attrName}`)"
      :text="attrValue"
    />
    <editable-avatar
      class="mx-auto avatar mt-16"
      v-model="profilePicture"
      @input="updateProfilePicture"
    />
  </v-card>
</template>

<script>
import { SEGMENT_EVENTS } from "@/helpers/constants/constants"
import TitleToText from "../../components/TitleToText"
import EditableAvatar from "../../components/Avatar/EditableAvatar"
import { mapActions } from "vuex"
import introjsSubscribeMixin from "../../mixins/introJs/introjsSubscribeMixin"

export default {
  name: "ConsumerProfile",
  components: {
    TitleToText,
    EditableAvatar,
  },
  mixins: [introjsSubscribeMixin],
  async mounted() {
    // get user details
    const [userDetails, userProfile] = await Promise.all([
      this.getUserDetails(),
      this.getProfile(),
    ])
    this.slug = userDetails.slug
    this.profilePicture = userProfile.profilePicture
    this.userAttributes = this.filterAttributes(userDetails)
  },

  data() {
    return {
      slug: null,
      userAttributes: null,
      profilePicture: null,
    }
  },

  methods: {
    ...mapActions("user", ["getUserDetails"]),
    ...mapActions("consumer", ["getProfile"]),
    ...mapActions("consumer", ["updateProfile"]),
    filterAttributes(userAttributes) {
      return { email: userAttributes["email"], name: userAttributes["name"] }
    },
    updateProfilePicture(profilePicture) {
      this.updateProfile({ slug: this.slug, profile: { profilePicture } })
      window.analytics.track(SEGMENT_EVENTS.profileEdited)
    },
  },
}
</script>
<style lang="scss" scoped>
.wrapper {
  max-width: 600px;
}
.avatar {
  width: 280px;
}
</style>
