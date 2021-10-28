<template>
  <v-row>
    <v-col lg="6" sm="12" xs="12">
      <v-card outlined class="d-flex flex-column fill-height">
        <span class="d-flex justify-center grey--text body-2 mb-0 mt-1">Stream details</span>
        <v-card-title>
          {{ stream.name }}
          <v-btn outlined color="primary" x-small class="ml-3" :href="serverUrl+'/streams/'+stream.id" target="_blank">View in Speckle.xyz</v-btn>
        </v-card-title>
        <v-card-subtitle>
          You are viewing the latest commit on this stream
        </v-card-subtitle>
        <v-card-text style="min-height: 180px; height:100%">
            <renderer show-selection-helper :object-urls="objectUrl"/>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col lg="6" sm="12" xs="12" class="d-flex flex-column">
        <v-card v-if="projectInfo" outlined class="d-flex flex-column fill-height">
          <span class="d-flex justify-center grey--text body-2 mb-0 mt-1">Revit project overview</span>
          <v-card-title>{{ projectInfo.name }} {{ projectInfo.number }}<span
              class="d-flex align-center text-body-2 grey--text border pl-2">
          <v-icon size="medium" color="grey"
                  class="pr-1">mdi-home-circle-outline</v-icon>{{ projectInfo.address }}</span>
          </v-card-title>
          <v-card-subtitle class="d-flex align-center">
            <v-icon size="small" class="pr-1">mdi-account-circle-outline</v-icon>
            {{ projectInfo.author }}
            <v-icon size="small" class="pr-1 pl-2">mdi-calendar-check-outline</v-icon>
            {{ projectInfo.status }}
          </v-card-subtitle>
          <v-row wrap dense class="d-flex align-center justify-center ma-3">
            <v-col v-for="(item, key) in totals" :key="key" class="col-4 d-flex flex-column justify-center align-center flex-fill">
              <div class="d-flex flex-column justify-center align-center flex-fill">
                <p class="text-md-h2 mb-0 primary--text">{{ item }}</p>
                <p class="pb-0 ma-0 primary--text caption">{{ key.toUpperCase() }}</p>
              </div>
            </v-col>
          </v-row>
        </v-card>
        <v-card v-else outlined class="d-flex justify-center align-center" height="100%">
          <v-card-subtitle>No project info was sent on this commit</v-card-subtitle>
        </v-card>
    </v-col>
  </v-row>
</template>

<script>
import {getStreamObject} from "@/speckleUtils";
import Renderer from "@/components/Renderer";

export default {
  name: "RevitProjectInfo",
  components: {Renderer},
  props: ["info", "stream", "totals"],
  data() {
    return {
      projectInfo: null,
      serverUrl: process.env.VUE_APP_SERVER_URL,
    }
  },
  computed: {
    objectUrl() {
      return [`${this.serverUrl}/streams/${this.stream.id}/objects/${this.stream.commits.items[0].referencedObject}`]
    }
  },
  watch: {
    info: {
      deep: true,
      immediate: true,
      handler: async function (val, oldVal) {
        if (!val) return
        var id = this.$route.params.id
        var res = await getStreamObject(id, this.info[0].referencedId)
        this.projectInfo = res
      }
    }
  }
}
</script>

<style scoped>
.renderer-parent {
  height: 200px;
  width: 400px;
  background-color: antiquewhite;
}
</style>