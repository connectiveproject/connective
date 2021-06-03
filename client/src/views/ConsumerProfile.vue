<template>
  <div class="wrapper mt-15 mx-auto px-3">
    <h1 class="mb-5">{{ $t("general.profile") }}</h1>
    <title-to-text
      v-for="attribute in userAttributes"
      :key="attribute.id"
      title=""
      text=""
    />
  </div>
</template>

<script>
// import store from "../vuex/store"
import TitleToText from "../components/TitleToText"
// import Avatar from "../components/Avatar/Avatar"
import { mapActions } from "vuex"

export default {
  components: {
    TitleToText,
    // Avatar,
  },

  async mounted() {
    const [userDetails, userProfile] = await Promise.all(
      this.updateUserDetails(),
      this.updateProfile()
    )
    console.log(userDetails, userProfile)
  },

  // data() {
  //   userAttributes: null
  // },

  methods: {
    ...mapActions("user", ["updateUserDetails"]),
    ...mapActions("consumer", ["updateProfile"]),
  },
}
// async beforeRouteEnter(to, from, next) {
//   try {
//     // fetch profile data before load
//     let profile = await store.dispatch("consumer/getProfile")
//     let userDetails = await store.dispatch("user/getUserDetails")
//     let userAttributes = { ...profile, ...userDetails }
//     next(vm => vm.setUserAttributes(userAttributes))
//   } catch (err) {
//     next(vm => (vm.popupMsg = vm.$t("errors.genericError")))
//   }
// },
</script>
