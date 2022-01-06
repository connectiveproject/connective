<template>
  <v-dialog v-model="dialog" width="540px">
    <v-card class="mx-auto" max-width="500">
      <v-list two-line>
        <v-list-item-group
          v-model="selected"
          active-class="primary--text"
          multiple
        >
          <template v-for="(item, index) in notificationList">
            <v-list-item :key="item.notification_code">
              <v-list-item-content>
                <v-list-item-title v-text="item.status"></v-list-item-title>

                <v-list-item-subtitle
                  class="text--primary"
                  v-text="item.createdAt"
                ></v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-divider
              v-if="index < notificationList.length - 1"
              :key="index"
            ></v-divider>
          </template>
        </v-list-item-group>
      </v-list>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from "vuex"

export default {
  async created() {
    const notifications = await this.loadNotificationList()
    this.notificationList = notifications["results"]
  },
  data: () => ({
    dialog: true,
    selected: [2],
    notificationList: [],
  }),
  methods: {
    ...mapActions("notification", ["getNotificationList"]),
    async loadNotificationList() {
      return this.getNotificationList()
    },
  },
}
</script>
