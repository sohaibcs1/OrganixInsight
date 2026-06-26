<template>
  
  <div>

    <div class="q-pa-sm q-gutter-sm text-black" v-if="expShow">
      <!-- Display Table Titles -->
      <div class="q-ml-sm q-gutter-md bg-grey-4">
        <div v-if="data.length > 0">
          <p><strong>Experiment Name:</strong> {{ tableTitles.experiment_name || 'N/A' }}</p>
          <p><strong>Experiment Date:</strong> {{ tableTitles.experiment_design_date || 'N/A' }}</p>
          <p><strong>Experiment Type:</strong> {{ tableTitles.ex_type || 'N/A' }}</p>
          <p><strong>Type:</strong> {{ tableTitles.type || 'N/A' }}</p>
          <p><strong>CoCulture:</strong> {{ tableTitles.coCulture || 'N/A' }}</p>
          <p><strong>Costain:</strong> {{ tableTitles.costain || 'N/A' }}</p>
          <p><strong>Counterstain:</strong> {{ tableTitles.counterstain || 'N/A' }}</p>
          <p><strong>Primary Antibody:</strong> {{ tableTitles.primary || 'N/A' }}</p>
          <p><strong>Secondary Antibody:</strong> {{ tableTitles.secondary || 'N/A' }}</p>
          <p><strong>Phase Info:</strong> {{ tableTitles.phase_info || 'N/A' }}</p>
          <p><strong>Magnification:</strong> {{ tableTitles.magnification || 'N/A' }}</p>
          <!-- <p><strong>Treatment Group:</strong> {{ tableTitles.treatment_group || 'N/A' }}</p> -->
        </div>
      </div>

      <!-- Data Table -->
      <q-table
        title="Treats"
        :rows="filteredRows"
        :columns="filteredColumns"
        :dense="$q.screen.lt.md"
        row-key="uuid"
        binary-state-sort
        table-header-style="background-color: #C0C0C0"
        style="background-color: #F5F5F5"
        class="q-table--dense compact-table"
        :pagination="pagination"
      >
        <template v-slot:top>
          <div class="q-pa-sm q-gutter-sm">
            <q-dialog v-model="show_dialog">
              <!-- Dialog Content -->
            </q-dialog>
          </div>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script>
import API from 'src/api';
import { ref } from 'vue';

export default {
  props: ['id_row', 'study_name'],
  data() {
    return {
      data: [], // Original data fetched from the API
      columns: [
        { name: 'name', align: 'center', label: 'Biospecimen', field: 'name', sortable: true },
        { name: 'harvest_time', align: 'center', label: 'Harvest Time', field: 'harvest_time', sortable: true },
        { name: 'drug', align: 'center', label: 'Drug', field: 'drug', sortable: true },
        { name: 'concentration', align: 'center', label: 'Drug Concentration', field: 'concentration', sortable: true },
        { name: 'treatment_group', align: 'center', label: 'Condition', field: 'treatment_group', sortable: true },

      ],
      tableTitles: {}, // To store extracted titles
      pagination: {
        rowsPerPage: null,
      },
      expShow: true,
      show_dialog: false,
      editedItem: {
        uuid: null,
        experiment_name: null,
        experiment_description: 'NA',
        experiment_notes: null,
        experiment_design_date: null,
      },
      defaultItem: {
        uuid: null,
        experiment_name: null,
        experiment_description: 'NA',
        experiment_notes: null,
        experiment_design_date: null,
      },
      editedIndex: -1,
    };
  },
  computed: {
    filteredRows() {
      return this.data.map(row => {
        const {
          comment, unit_harvest, time, concentration, unit_drug, ...rest
        } = row;

        rest.harvest_time = time && unit_harvest ? `${time} ${unit_harvest}` : 'N/A';
        rest.concentration = concentration && unit_drug ? `${concentration} ${unit_drug}` : 'N/A';
        rest.drug = row.drug || 'N/A';
        return rest;
      });
    },
    filteredColumns() {
      const columnsToCheck = ['drug', 'concentration'];
      const validColumns = new Set();

      this.filteredRows.forEach(row => {
        columnsToCheck.forEach(column => {
          if (row[column] && row[column] !== 'N/A') validColumns.add(column);
        });
      });

      return this.columns.filter(column => validColumns.has(column.name) || !columnsToCheck.includes(column.name));
    },
  },
  methods: {
    setTableTitles(index) {
      if (this.data[index]) {
        const { experiment_name,experiment_design_date, ex_type, type, coCulture, costain, counterstain, primary, secondary, magnification, phase_info } =
          this.data[index];

        this.tableTitles = {
          experiment_name,
          experiment_design_date,
          ex_type,
          type,
          coCulture,
          costain,
          counterstain,
          primary,
          secondary,
          magnification,
          phase_info,
        };
      }
    },
    async addRow() {
      const { uuid, experiment_name, experiment_description, experiment_design_date } = this.editedItem;
      const study_id = this.id_row;

      if (this.editedIndex > -1) {
        Object.assign(this.data[this.editedIndex], this.editedItem);
        await API('auth.update_experiment', {
          id: uuid,
          experiment_name,
          experiment_description,
          experiment_design_date,
          study_id,
        });
      } else {
        if (experiment_name && experiment_description && experiment_design_date && study_id) {
          const response = await API('auth.create_obj_experiment', {
            experiment_name,
            experiment_description,
            experiment_design_date,
            study_id,
          });
          if (response !== 'exist') {
            this.data.push(this.editedItem);
          } else {
            this.$q.notify({ message: 'Already Exist.', color: 'red', icon: 'announcement' });
          }
        } else {
          this.$q.notify({ message: 'Please Enter all Details.', color: 'red', icon: 'announcement' });
        }
      }
      this.close();
    },
    async deleteItem(item) {
      const index = this.data.indexOf(item);
      if (confirm('Are you sure you want to delete this experiment?')) {
        this.data.splice(index, 1);
        await API('auth.deleteExperiment', { id: item.uuid });
      }
    },
    close() {
      this.show_dialog = false;
      setTimeout(() => {
        this.editedItem = { ...this.defaultItem };
        this.editedIndex = -1;
      }, 300);
    },
  },
  mounted() {
    const key = this.id_row;
    API('auth.ExperimentDetials_id', { key }).then(res => {
      this.data = res;
      if (this.data.length > 0) {
        this.setTableTitles(0); // Default to first experiment initially
      }
    });
  },
};
</script>

<style>
.compact-table td {
  padding: 0px 0px !important;
}
</style>
