<template lang="html">
  <v-container fill-height fluid class="pa-0">
    <div class="float-center-top">
      <CommitPanel
        v-if="stream"
        :showDiff.sync="showDiff"
        :diffCommit.sync="diffCommit"
        :currentCommit.sync="currentCommit"
        :prevCommit.sync="prevCommit"
        :commits="stream.branch.commits.items"
      />
    </div>
    <v-row class="fill-height" no-gutters v-show="!showDiff">
      <v-col cols="6">
        <Renderer
          :object-url="objectUrl(currentCommit)"
          show-selection-helper
        ></Renderer>
      </v-col>
      <v-col cols="6">
        <Renderer
          :object-url="objectUrl(prevCommit)"
          show-selection-helper
        ></Renderer>
      </v-col>
    </v-row>
    <v-row class="fill-height" no-gutters>
      <v-col fill-height :cols="12">
        <Renderer
          :object-url="objectUrl(diffCommit)"
          show-selection-helper
        ></Renderer>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { getStreamCommits } from "@/speckleUtils"
import Renderer from "../components/viewer/Renderer.vue"
import CommitPanel from "@/components/commitSelector/CommitPanel.vue"

export default {
  name: "StreamView",
  components: { Renderer, CommitPanel },
  data() {
    return {
      stream: null,
      currentCommit: null,
      prevCommit: null,
      diffCommit: null,
      serverUrl: process.env.VUE_APP_SERVER_URL,
      showDiff: false,
      loading: true
    }
  },
  async mounted() {
    if (this.streamId) {
      this.getStream()
    }
  },
  computed: {
    /** @return {string} */
    streamId() {
      return this.$route.params.id
    }
  },
  methods: {
    async getStream() {
      var res = await getStreamCommits(this.streamId, 10, null)
      this.stream = res.data.stream
    },
    objectUrl(commit) {
      if (!commit) return null
      return `${this.serverUrl}/streams/${this.stream.id}/objects/${commit.referencedObject}`
    }
  },
  watch: {
    streamId: {
      handler: async function(val, oldVal) {
        if (val) this.getStream()
      }
    }
  }
}
</script>

<style scoped>
.bg-img {
  background-position: center;
  background-repeat: no-repeat;
  /*background-attachment: fixed;*/
}

.max-h {
  max-height: 400px;
  height: 400px;
}

.float-center-top {
  position: absolute;
  display: flex;
  left: 50%;
  max-width: 80%;
  transform: translatex(-50%);
  top: 1em;
  z-index: 3;
}
</style>
