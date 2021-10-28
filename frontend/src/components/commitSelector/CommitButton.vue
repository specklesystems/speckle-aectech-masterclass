<template lang="html">
  <v-hover v-slot="{ hover }">
    <div
      :class="{
        primary: !hover & !selected,
        'primary lighten-2': hover & !selected,
        success: !hover & selected,
        'success darken-2': hover & selected
      }"
      class="pa-2 commit-button d-flex justify-center align-center rounded"
      @click="onClick"
    >
      A
    </div>
  </v-hover>
</template>

<script>
export default {
  data() {
    return {
      selected: false
    }
  },
  methods: {
    onClick(event) {
      this.selected = !this.selected
    }
  }
}
</script>

<style>
.commit-button {
  cursor: pointer;
  min-height: 60px;
}
</style>
