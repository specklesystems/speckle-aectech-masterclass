<template lang="html">
  <v-container fill-height fluid class="pa-0 grey lighten-3">
    TODO: Code up the stream diff view!!!
  </v-container>
</template>

<script>
import { getStreamCommits } from "@/speckleUtils"
import Renderer from "../components/viewer/Renderer.vue"
import CommitPanel from "@/components/commitSelector/CommitPanel.vue"

export default {
  name: "StreamView",
  components: {},
  data() {
    return {
      stream: null,
      currentCommit: null,
      prevCommit: null,
      diffCommit: null,
      serverUrl: process.env.VUE_APP_SERVER_URL,
      showDiff: false
    }
  },
  async mounted() {
    //TODO: Get stream when mounting view
  },
  computed: {
    /** @return {string} */
    streamId() {
      return this.$route.params.id
    }
  },
  methods: {
    async getStream() {
      //TODO: Missing implementation
    },
    objectUrl(commit) {
      //TODO: Missing implementation
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
