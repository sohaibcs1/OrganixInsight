<template>
  <div>
    <!-- Form section -->
    <div class="q-pa-sm q-gutter-sm text-black">
      <div class="text-h6 text-center">Antibodies</div>
      <div class="fit">
        <div class="row justify-center fit">
          <div class="text-center q-mr-lg">
            <q-btn
              color="green"
              label="ADD New Antibody"
              @click="clearSelection(); addNewTable();"
            ></q-btn>
          </div>

          <q-input v-model="activeTable.editedItem.uuid" label="Id:" hidden />
          <q-select
            outlined
            v-model="activeTable.editedItem.primary"
            :options="optionsPrimary"
            hint="Max 1 selection"
            label="Primary Antibody"
            stack-label
            dense
            style="min-width: 300px; font-size: 12px;"
          />
          <q-select
            outlined
            v-model="activeTable.editedItem.secondry"
            :options="optionsSecondary"
            hint="Max 1 selection"
            label="Secondary Antibody"
            stack-label
            dense
            style="min-width: 300px; font-size: 12px;"
          />
          <q-select
            outlined
            v-model="activeTable.editedItem.costain"
            :options="optionsConcentration"
            hint="Max 1 selection"
            label="Costain"
            stack-label
            dense
            style="min-width: 300px; font-size: 12px;"
          />

          <q-input
            type="number"
            outlined
            v-model="activeTable.editedItem.concentration_primary"
            stack-label
            label="Concentration Primary"
            dense
            style="max-width: 220px; font-size: 12px;"
          />

          <q-select
            outlined
            v-model="activeTable.editedItem.unit_primary"
            input-debounce="0"
            use-input
            :options="optionsPrimaryUnits"
            counter
            max-values="1"
            hint="Max 1 selection"
            label="Primary Antibody Unit"
            stack-label
            dense
            style="max-width: 220px; font-size: 12px;"
          />

          <q-input
            type="number"
            outlined
            v-model="activeTable.editedItem.concentration_secondary"
            stack-label
            label="Concentration Secondary"
            dense
            style="max-width: 220px; font-size: 12px;"
          />

          <q-select
            outlined
            v-model="activeTable.editedItem.unit_secondary"
            input-debounce="0"
            use-input
            :options="optionsSecondaryUnits"
            counter
            max-values="1"
            hint="Max 1 selection"
            label="Secondary Antibody Unit"
            stack-label
            dense
            style="max-width: 220px; font-size: 12px;"
          />

          <div class="text-center q-ml-xl">
            <q-btn
              style="width: 100px"
              color="black"
              label="ADD"
              @click="addRow(); perform(); handleselection(); handleselection2();"
              :disable="disableButton"
            ></q-btn>
          </div>
        </div>
      </div>
    </div>

    <!-- Table section -->
    <div v-for="(table, index) in tables" :key="index">
      <q-table
        v-if="table.show"
        :rows="table.data"
        :columns="columns"
        :dense="$q.screen.lt.md"
        :row-key="table.rowKey"
        :max-width="table.maxWidth"
        :binary-state-sort="table.binaryStateSort"
        :table-header-style="table.tableHeaderStyle"
        :class="table.className"
        :pagination="table.pagination"
      >
        <template v-slot:body-cell-actions="props">
          <q-td key="actions" :props="props">
            <q-btn
              color="red"
              label="Delete"
              icon="delete"
              @click="deleteItem(props.row)"
              size="11px"
              class="q-mr-sm"
            ></q-btn>
          </q-td>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import API from "src/api";

export default {
  setup() {
    const optionsConcentration = ref(["True", "False"]);
    const optionsPrimaryUnits = ref(["mg/ml", "ug/ml", "ng/ml"]);
    const optionsSecondaryUnits = ref(["mg/ml", "ug/ml", "ng/ml"]);

    const columns = [
      {
        name: "desc",
        required: true,
        label: "Primary",
        align: "center",
        field: (row) => row.primary,
        format: (val) => `${val}`,
        sortable: true,
      },
      { name: "three", align: "center", label: "Secondary", field: "secondry", sortable: true },
      { name: "four", align: "center", label: "Costain", field: "costain", sortable: true },
      { name: "five", align: "center", label: "Concentration Primary", field: "concentration_primary", sortable: true },
      { name: "six", align: "center", label: "Primary Unit", field: "unit_primary", sortable: true },
      { name: "seven", align: "center", label: "Concentration Secondary", field: "concentration_secondary", sortable: true },
      { name: "eight", align: "center", label: "Secondary Unit", field: "unit_secondary", sortable: true },
      { name: "actions", align: "center", label: "Actions", field: "actions" },
    ];

    const tables = ref([
      {
        data: [],
        columns: columns,
        rowKey: "name",
        maxWidth: "100%",
        binaryStateSort: true,
        tableHeaderStyle: "background-color: #C0C0C0",
        className: "q-table--dense",
        pagination: {
          rowsPerPage: 10,
        },
        show: true,
        editedItem: ref({
          uuid: Math.floor(Math.random() * 1000).toString(),
          primary: [],
          secondry: [],
          costain: [],
          concentration_primary: null,
          unit_primary: null,
          concentration_secondary: null,
          unit_secondary: null,
        }),
      },
    ]);

    const addRow = () => {
      const {
        primary,
        secondry,
        costain,
        concentration_primary,
        unit_primary,
        concentration_secondary,
        unit_secondary,
      } = activeTable.value.editedItem;

      if (primary.length > 0 && secondry.length > 0 && costain.length > 0) {
        const newItem = {
          uuid: activeTable.value.editedItem.uuid,
          primary,
          secondry,
          costain,
          concentration_primary,
          unit_primary,
          concentration_secondary,
          unit_secondary,
        };
        activeTable.value.data.push(newItem);
      }
    };

    const deleteItem = (row) => {
      const index = activeTable.value.data.findIndex((item) => item.uuid === row.uuid);
      if (index !== -1) {
        activeTable.value.data.splice(index, 1);
      }
    };

    const perform = () => {
      disableButton.value = activeTable.value.editedItem.costain.includes("False");
    };

    const clearSelection = () => {
      activeTable.value.editedItem.costain = [];
      disableButton.value = false;
    };

    const tablesData = computed(() => {
      return tables.value.map((table) => table.data);
    });

    const handleselection = () => {
      const parsedData = parseData(tablesData.value);
      const rawData = parsedData.map((sublist) =>
        sublist.map((item) => JSON.parse(JSON.stringify(item)))
      );
      emit("childMessage", rawData);
    };

    const handleselection2 = () => {
      combi(all).then((result) => {
        emit("childMessage2", all);
      });
    };

    const parseData = (input_data) => {
      let parsed_data = {};
      for (let sublist of input_data) {
        for (let item of sublist) {
          let uuid = item.uuid;
          if (!parsed_data[uuid]) {
            parsed_data[uuid] = [];
          }
          parsed_data[uuid].push(item);
        }
      }
      return Object.values(parsed_data);
    };

    const combi = async (json_array) => {
      let combined_object = {};
      for (const obj of json_array) {
        for (const key in obj) {
          if (obj.hasOwnProperty(key)) {
            if (!(key in combined_object)) {
              combined_object[key] = obj[key];
            } else {
              combined_object[key] += ", " + obj[key];
            }
          }
        }
      }
      return [combined_object];
    };

    const activeTableIndex = ref(0);
    const activeTable = computed(() => tables.value[activeTableIndex.value]);

    const disableButton = ref(false);

    return {
      optionsPrimary: ref([]),
      optionsSecondary: ref([]),
      optionsConcentration,
      optionsPrimaryUnits,
      optionsSecondaryUnits,
      columns,
      tables,
      activeTable,
      addRow,
      deleteItem,
      perform,
      clearSelection,
      tablesData,
      handleselection,
      handleselection2,
      parseData,
      combi,
      disableButton,
    };
  },

  mounted() {
    API("auth.Immunofluorescent_details_Antibody_primary").then((res) => {
      this.optionsPrimary = res.map((item) => item.type_id);
    });

    API("auth.Immunofluorescent_details_Antibody_secondry").then((res) => {
      this.optionsSecondary = res.map((item) => item.type_id);
    });
  },
};
</script>

<style scoped></style>
