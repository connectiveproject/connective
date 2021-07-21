<template>
  <v-card
    class="wrapper mt-15 mx-auto px-10 py-10"
    :elevation="$vuetify.breakpoint.mobile ? 0 : 3"
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
import TitleToText from "../../components/TitleToText"
import EditableAvatar from "../../components/Avatar/EditableAvatar"
import { mapActions } from "vuex"

export default {
  components: {
    TitleToText,
    EditableAvatar,
  },

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
    },
  },
}
</script>
<style lang="scss" scoped>
.wrapper {
  max-width: 600px;
}
.avatar {
  width: 300px;
}
</style>
