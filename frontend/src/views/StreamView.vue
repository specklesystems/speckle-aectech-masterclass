<template lang="html">
  <v-container fill-height fluid class="pa-0">
    <div class="float-center-top">
      <CommitPanel v-if="stream" :commits="stream.commits.items"></CommitPanel>
    </div>
    <v-row class="fill-height" no-gutters>
      <v-col fill-height cols="6">
        <Renderer
          v-if="stream"
          :object-urls="[objectUrl(0)]"
          show-selection-helper
        ></Renderer>
      </v-col>
      <v-col fill-height cols="6">
        <Renderer
          v-if="stream"
          :object-urls="[objectUrl(1)]"
          show-selection-helper
        ></Renderer>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { getStreamCommits, getStreamObject } from "@/speckleUtils"
import Renderer from "../components/viewer/Renderer.vue"
import CommitPanel from "@/components/commitSelector/CommitPanel.vue"

export default {
  name: "StreamView",
  components: { Renderer, CommitPanel },
  data() {
    return {
      stream: null,
      selectedCommit: null,
      refObj: null,
      serverUrl: process.env.VUE_APP_SERVER_URL,
      loading: true,
      progress: 0
    }
  },
  async mounted() {
    if (this.streamId) {
      this.getStream()
    }
  },
  computed: {
    streamId() {
      return this.$route.params.id
    }
  },
  methods: {
    async getStream() {
      var res = await getStreamCommits(this.streamId, 10, null)
      this.selectedCommit = res.data.stream.commits.items[0]
      this.stream = res.data.stream
    },
    objectUrl(i) {
      return [
        `${this.serverUrl}/streams/${this.stream.id}/objects/${this.stream.commits.items[i].referencedObject}`
      ]
    }
  },
  watch: {
    streamId: {
      handler: async function(val, oldVal) {
        if (val) this.getStream()
      }
    },
    selectedCommit: {
      handler: async function() {
        this.refObj = await getStreamObject(
          this.stream.id,
          this.selectedCommit.referencedObject
        )
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
