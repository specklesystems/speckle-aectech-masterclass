<template>
  <div>
    <revit-project-info :info="info" :stream="stream" :totals="totals"/>
    <v-row>
      <v-col cols="12">
        <v-card max-height="500px" outlined>
          <v-card-title>Objects by category</v-card-title>
          <v-card-text>
            <doughnut-chart ref="doughnut" v-if="objsByCategoryData" :chart-data="objsByCategoryData"
                            :options="doughnutOptions"></doughnut-chart>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col lg="6" sm="12" xs="12">
        <v-card max-height="500px" min-height="500px" outlined>
          <v-card-title>Elements Per Level/Category</v-card-title>
          <v-card-text>
            <horizontal-barchart v-if="objsByLevelData" :chart-data="objsByLevelData"
                                 :options="options"></horizontal-barchart>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col lg="6" sm="12" xs="12">
        <v-card max-height="500px" min-height="500px" outlined>
          <v-card-title>Families<v-badge inline :content="totals.families"></v-badge> and Types <v-badge inline :content="totals.types"></v-badge></v-card-title>
          <v-card-subtitle>
            <v-text-field dense clearable prepend-icon="mdi-filter" placeholder="Filter all family types"
                          v-model="typeFilter"></v-text-field>
          </v-card-subtitle>
          <v-card-text>
            <v-treeview dense :items="familyTypeTree" :search="typeFilter"></v-treeview>

          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import ObjectLoader from '@speckle/objectloader'
import HorizontalBarchart from "@/components/charts/HorizontalBarchart";
import interpolate from "color-interpolate";
import DoughnutChart from "@/components/charts/DoughnutChart";
import RevitProjectInfo from "@/components/RevitProjectInfo";
import {TOKEN} from "@/speckleUtils";

function debounce(callback, wait) {
  let timerId;
  return (...args) => {
    clearTimeout(timerId);
    timerId = setTimeout(() => {
      callback(...args);
    }, wait);
  };
}

export default {
  name: "RevitDashboard",
  components: {RevitProjectInfo, DoughnutChart, HorizontalBarchart},
  props: ["streamId", "objectId", "revitData", "info", "stream"],
  data() {
    return {
      familyTypeTree: [],
      typeFilter: "",
      loader: null,
      objsPerLevel: null,
      colorRange: interpolate(["#047EFB", "#4caf50"]),
      availableLevels: {},
      availableFamTypes: null,
      totals: {
        levels: 0,
        elements: 0,
        views: 0,
        families: 0,
        types: 0
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            stacked: true,
            categoryPercentage: 0.5,
            barPercentage: 1
          }],
          yAxes: [{
            stacked: true
          }]
        }
      },
      doughnutOptions: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          position: 'left',
          onClick: (e, legendItem) => {
            this.$emit("legend-clicked", e, legendItem)
          }
        },
        pieceLabel: {
          mode: 'value',
          precision: 0,
          fontSize: 18,
          fontColor: '#fff',
          fontStyle: 'bold',
        }
      },
    }
  },
  computed: {
    objsByLevelData() {
      // Fast exit if no object has been set yet
      if (!this.objsPerLevel) return null

      var labels = []
      var dataSets = []
      var count = 0
      // Loop through categories
      for (const [key, value] of Object.entries(this.objsPerLevel)) {
        // Create empty data set
        let dataSet = {
          label: key,
          backgroundColor: this.colorRange(count / Object.keys(this.objsPerLevel).length),
          data: []
        }
        count++
        // Loop through levels on each category
        for (const [lvlKey, lvlValue] of Object.entries(value)) {
          // Append level name to labels if it hasn't already
          if (labels.indexOf(lvlKey) === -1) labels.push(lvlKey)
          // Push category count per level to dataset data
          dataSet.data.push(Object.keys(lvlValue).length)
        }
        // Add dataset to list
        dataSets.push(dataSet)
      }
      return {
        labels,
        datasets: dataSets,
      }
    },
    objsByCategoryData() {
      // Fast exit if no object has been set yet
      if (!this.objsPerLevel) return null

      var labels = []
      var count = 0
      let dataSet = {
        backgroundColor: [],
        data: []
      }
      // Loop through categories
      for (const [key, value] of Object.entries(this.objsPerLevel)) {
        // Loop through levels on each category
        labels.push(key)
        dataSet.backgroundColor.push(this.colorRange(count / Object.keys(this.objsPerLevel).length))
        var total = 0
        for (const [_, lvlValue] of Object.entries(value)) {
          // Push category count per level to dataset data
          total += Object.keys(lvlValue).length
        }
        dataSet.data.push(total)
        count++
      }
      return {
        labels,
        datasets: [dataSet],
      }

    }
  },
  async mounted() {
    this.processStreamObjects()
  },
  watch: {
    streamId: {
      handler: function (val, oldVal) {
        this.processStreamObjects()
      }
    },
    objectId: {
      handler: function (val, oldVal) {
        this.processStreamObjects()
      }
    },
    availableFamTypes: {
      handler: function(val, oldVal) {
        this.familyTypeTree = this.famTypeTree();
      }
    }
  },
  methods: {
    famTypeTree() {
      var totalFams = 0
      var totalTypes = 0
      if (!this.availableFamTypes) return []
      var id = 0;
      var items = []
      // Iterate through the categories
      Object.entries(this.availableFamTypes).forEach(([key, val]) => {
        var children = []
        // Iterate through the families
        Object.entries(val).forEach(([childKey, childVal]) => {
          var grandChilds = []
          // Iterate through available types
          Object.entries(childVal).forEach(([grandKey, grandVal]) => {
            grandChilds.push({
              id: id++,
              name: grandKey
            })
            totalTypes++
          })
          children.push({
            id: id++,
            name: childKey,
            children: grandChilds
          })
          totalFams++
        })
        items.push({
          id: id++,
          name: key,
          children: children
        })
      })
      this.totals.families = totalFams
      this.totals.types = totalTypes
      return items
    },
    async processStreamObjects() {
      this.$emit("loaded", false)
      this.$emit("progress", 0)

      this.loader = new ObjectLoader({
        serverUrl: process.env.VUE_APP_SERVER_URL,
        streamId: this.stream.id,
        objectId: this.objectId,
        token: localStorage.getItem(TOKEN)
      })

      function shouldIgnore(obj) {
        return obj.speckle_type.startsWith("Objects.Geometry") ||
            obj.speckle_type.endsWith("DataChunk") ||
            obj.speckle_type.endsWith("GridLine") ||
            obj.speckle_type.endsWith("ElementType") ||
            obj.speckle_type === "Base" ||
            obj.speckle_type.endsWith("ProjectInfo")
      }

      // Initialize placeholders
      const typeCategoryMap = {}
      const objectsPerLevel = {}
      const availableCategoriesAndTypes = {}
      const availableLevels = {}
      var totalViews = 0
      var totalElements = 0
      var total = 0
      var count = 0
      var d = debounce(() => {

      }, 10)
      for await (let obj of this.loader.getObjectIterator()) {
        if (!total) total = obj.totalChildrenCount
        var progress = Math.floor((count * 100) / total)
        this.$emit("progress", progress)
        count++
        // Get all types in the document
        if (obj.speckle_type.endsWith("ElementType")) {
          typeCategoryMap[obj.type] = obj.category // Map type to category

          // Ensure structure exists
          if (!availableCategoriesAndTypes[obj.category])
            availableCategoriesAndTypes[obj.category] = {}
          if (!availableCategoriesAndTypes[obj.category][obj.family])
            availableCategoriesAndTypes[obj.category][obj.family] = {}

          // Assign
          availableCategoriesAndTypes[obj.category][obj.family][obj.type] = obj
          continue
        }

        // Get all views in the document
        if (obj.speckle_type === "Objects.BuiltElements.View" || obj.speckle_type === "Objects.BuiltElements.View:Objects.BuiltElements.View3D") {
          totalViews++
          continue
        }

        // Should we ignore this object?
        if (shouldIgnore(obj)) continue

        // Increase element count
        totalElements++

        var rvtType = obj.type || "Other"
        var lvl = obj.level?.name || "No level"

        // If object has level, cache it.
        if (lvl !== "No level" && !availableLevels[lvl]) {
          availableLevels[lvl] = obj.level
        }

        // Make sure nested structure exists
        if (!objectsPerLevel[rvtType])
          objectsPerLevel[rvtType] = {}
        if (!objectsPerLevel[rvtType][lvl])
          objectsPerLevel[rvtType][lvl] = {}

        // Assign obj
        objectsPerLevel[rvtType][lvl][obj.elementId] = obj
      }

      // Load has finished, post-process data

      // Organize categories per level
      var catsPerLevel = {}
      Object.keys(objectsPerLevel).forEach(fam => {
        var value = objectsPerLevel[fam]
        var cat = typeCategoryMap[fam]
        if (!catsPerLevel[cat]) catsPerLevel[cat] = {}
        Object.keys(value).forEach(levelKey => {
          if (!catsPerLevel[cat][levelKey]) catsPerLevel[cat][levelKey] = {}
          catsPerLevel[cat][levelKey] = {...catsPerLevel[cat][levelKey], ...objectsPerLevel[fam][levelKey]}
        })
      })

      this.objsPerLevel = catsPerLevel
      this.availableFamTypes = availableCategoriesAndTypes
      this.availableLevels = availableLevels
      this.totals.levels = Object.keys(this.availableLevels).length
      this.totals.views = totalViews
      this.totals.elements = totalElements

      this.$emit("loaded", true)
    }
  }
}
</script>

<style scoped>
.scroll-box {
  overflow: scroll;
  padding: 1em;
}

.v-card {
  display: flex !important;
  flex-direction: column;
}

.v-card__text {
  flex-grow: 1;
  overflow: auto;
}
</style>