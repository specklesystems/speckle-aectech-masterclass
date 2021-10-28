<template lang="html">
  <v-container fill-height fluid class="pa-0">
    <div class="float-center-top">
      <CommitPanel></CommitPanel>
    </div>
    <Renderer v-if="refObj" :object-urls="[objectUrl]"></Renderer>
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
    },
    objectUrl() {
      return [
        `${this.serverUrl}/streams/${this.stream.id}/objects/${this.selectedCommit.referencedObject}`
      ]
    }
  },
  methods: {
    async getStream() {
      var res = await getStreamCommits(this.streamId, 1, null)
      this.selectedCommit = res.data.stream.commits.items[0]
      this.stream = res.data.stream
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
  transform: translatex(-50%);
  top: 1em;
  z-index: 3;
}
</style>
