<template>
  <v-dialog v-model="dialog" width="700px" @click:outside="close">
    <v-card class="mx-auto" max-width="700">
      <v-list two-line>
        <v-list-item-group>
          <v-list-item
            two-line
            v-for="(item, index) in notificationList"
            :key="index"
          >
            <v-list-item-content>
              <v-list-item-title
                v-text="
                  $t(item.titleLabel, convertParamsToObject(item.parameters))
                "
                :class="item.status"
                @click="goToLink(item)"
              ></v-list-item-title>
              <v-list-item-subtitle
                v-text="formatApiDate(item.createdAt)"
                :class="item.status"
                @click="goToLink(item)"
              ></v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-action @click="deleteItem(item)">
              <v-icon color="error"> mdi-delete </v-icon>
            </v-list-item-action>
          </v-list-item>
          <template v-if="notificationList.length === 0">
            {{ $t("notifications.emptyList") }}
          </template>
        </v-list-item-group>
      </v-list>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from "vuex"
import Utils from "@/helpers/utils"

export default {
  async created() {
    await this.loadNotifications()
    if (this.notificationList.length > 0) {
      const latestNotificationSlug = this.notificationList[0].slug
      // after 3 seconds we consider all visible notifications as "read":
      await setTimeout(() => this.markAsRead(latestNotificationSlug), 3000)
    }
  },

  data: () => ({
    dialog: true,
    selected: [2],
    notificationList: [],
  }),
  methods: {
    ...mapActions("notification", [
      "getNotificationList",
      "dismissNotification",
      "markAllAsRead",
      "setVisible",
    ]),
    checkRtl: Utils.checkRtl,

    async loadNotifications() {
      const notifications = await this.getNotificationList()
      this.notificationList = notifications["results"]
    },

    convertParamsToObject(parametersStr) {
      if (!parametersStr) return ""
      return JSON.parse(parametersStr.replaceAll("'", '"'))
    },

    formatApiDate(date) {
      return Utils.ApiStringToReadableDate(date)
    },

    async deleteItem(item) {
      await this.dismissNotification({ slug: item.slug })
      await this.loadNotifications()
    },
    goToLink(item) {
      this.$router.push({
        name: item.link,
        params: item.linkParameters,
      })
      this.close()
    },
    async markAsRead(maxSlug) {
      await this.markAllAsRead({ maxSlug: maxSlug })
    },
    close() {
      this.setVisible(false)
      this.$emit("close", false)
    },
  },
}
</script>
<style scoped>
.NEW {
  font-weight: bold;
}
</style>
