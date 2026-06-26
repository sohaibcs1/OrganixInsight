<template>

  <div>
    <div class="q-pa-sm q-gutter-sm">
      <div class="text-center text-black text-h6">Epithelial</div>

      <q-table
        title="Treats"
        :rows="data"
        :columns="columns"
        :dense="$q.screen.lt.md"
        row-key="name"
        max-width="100%"
        binary-state-sort
        table-header-style="background-color: #C0C0C0"
        style="background-color: #F5F5F5; font-size: 8px;"
        class="q-table--dense compact-table"
        :pagination="pagination"
        separator="horizontal"
      >
        <template v-slot:top>
          <div class="q-pa-sm q-gutter-sm"></div>
        </template>

        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td key="desc" :props="props">
              <q-badge color="grey-6" class="text-white text-caption" >
                {{ props.row.type_id }}
              </q-badge>
            </q-td>



            <q-td key="actions" :props="props">
              <q-btn
                color="black"
                label="Attributes"
                icon-right="add"
                @click="
                  show_dialog_attributes = true;
                  getid(props.row);
                "
                v-model="props.row.uuid"
                size="11px"
                class="q-mr-sm"
                dense
              ></q-btn>

              <q-btn
                color="red"
                label="Delete"
                icon-right="delete"
                @click="deleteItem(props.row)"
                size="11px"
                dense
              ></q-btn>

            </q-td>
          </q-tr>
        </template>
      </q-table>
      <div class="text-center">
      <q-btn
        color="black"
        label="Add New Epithelial"
        icon-right="note_add"
        @click="show_dialog = true"
        dense
      ></q-btn>
    </div>
    </div>


    <q-dialog v-model="show_dialog">
      <q-card style="width: 230px; max-width: 230px; background-color: #F5F5F5">
        <q-card-section>
          <div class="text-h6 text-center bg-grey-5">Add Epithelial</div>
        </q-card-section>

        <q-card-section align="center">
          <div class="row text-center">
            <q-input v-model="editedItem.uuid" label="Id:" hidden />

            <q-input
              outlined
              v-model="editedItem.type_id"
              placeholder="Epithelial Name"
              stack-label
              :rules="[
                (val) => (val && val.length > 0) || 'Please type something',
              ]"
              dense
            /><q-space />
          </div>
        </q-card-section>

        <q-card-actions align="center">
          <div class="text-center q-mr-lg">
            <q-btn dense color="black" v-close-popup label="Cancel"></q-btn>
          </div>
          <div class="text-center">
            <q-btn
              dense
              color="black"
              v-close-popup
              label="OK"
              @click="addRow"
            ></q-btn>
          </div>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="show_dialog_attributes">
      <q-card
        style="width: 1000px; max-width: 1000px; background-color: #F5F5F5"
      >


        <q-card-section align="center">
          <div class="row text-center">
            <biospecimenCell_attri
              :id_row="idParamenterRow" :type_biosp="typeBio"
              class="fit"
            ></biospecimenCell_attri>
          </div>
        </q-card-section>


      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import API from "src/api";
import { ref } from "vue";
import { exportFile, useQuasar } from "quasar";

import biospecimenCell_attri from "src/components/admin/biospecimenCell_attri";

const columns = [
  {
    name: "desc",
    required: true,
    label: "Name",
    align: "center",
    field: (row) => row.type_id,
    format: (val) => `${val}`,
    sortable: true,
  },

  { name: "actions", align: "center", label: "Actions", field: "actions" },
];

var listLocation = [];
var listRoute = [];

const stringOptionsCam = listLocation;
const stringOptionsRoute = listRoute;
const stringOptionsRole = ["admin", "officer"];

export default {

  setup() {
    const $q = useQuasar();
    const optionsCam = ref(stringOptionsCam);
    const optionsRoute = ref(stringOptionsRoute);
    const optionsRole = ref(stringOptionsRole);

    return {
      pagination: {
        rowsPerPage: 100 // current rows per page being displayed
      },
      listLocation,
      listRoute,

      idParamenterRow: null,
      typeBio:null,

      columns,
      show_dialog: ref(false),
      show_dialog_attributes: ref(false),
      editedIndex: -1,
      userD: ref(false),
      // editedItem: ref({
      //   uuid: ref(null),
      //   type_id: ref(null),
      //   type:ref(null),
      // }),
      // defaultItem: ref({
      //   uuid: ref(null),
      //   type_id: ref(null),
      //   type:ref(null),
      // }),
      editedItem: ref({
      uuid: null,
      type_id: null,
      type: "Epithelial",
    }),
    defaultItem: {
      uuid: null,
      type_id: null,
      type: "Epithelial",
    },

      optionsCam,
      optionsRoute,
      optionsRole,

      filterRole(val, update, abort) {
        update(() => {
          const needle = val.toLowerCase();
          optionsRole.value = stringOptionsRole.filter(
            (v) => v.toLowerCase().indexOf(needle) > -1
          );
        });
      },
    };
  },
  components: { biospecimenCell_attri },
  methods: {
    async addRow() {
      const id1 = this.editedItem.uuid;
      const type_id1 = this.editedItem.type_id;
      const type1="Epithelial"
      const editedIndex1 = this.editedIndex;
      const oldRow = this.data[editedIndex1];
      const updatedRow = this.editedItem;

      if (this.editedIndex > -1) {
        Object.assign(oldRow, updatedRow) ;
        // this.data[editedIndex1] = updatedRow;
          API("auth.updateBiospecimen", { id1: id1, type_id: type_id1 });
      } else {
        if (type_id1) {
          this.data.push(this.editedItem) ;
          console.log("Added row:", type_id1,type1); // Debugging line: Check the added row data

          await API("auth.createBiospecimen", { type_id: type_id1, type:type1 });
        } else {
          this.$q.notify({
            message: "please Enter all Details.",
            color: "red",
            icon: "announcement",
          });
        }
      }
      // after adding update
         API("auth.bioSpecimenDetials_distinct_type_id").then((res) => {
      this.data = res;
      console.log(this.data)
    });
      this.close();
    },

    getid(item) {
      const id = item.type_id;
      const t = item.type;
      this.idParamenterRow = id;
      this.typeBio=t;
      // console.log(id + "oooo")
    },
    async deleteItem(item) {
      const id = item.uuid;
      // console.log(id + "oooo")
      const index = this.data.indexOf(item);
      confirm("Are you sure you want to Delete this user?") &&
        this.data.splice(index, 1) &&
        (await API("auth.deleteBiospecimen", { id }));
    },
    async editItem(item) {
      this.editedIndex = this.data.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.show_dialog = true;
    },
    async close() {
      this.show_dialog = false;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    },
  },

  data: () => ({
    data: [],
  }),

  mounted() {

    API("auth.bioSpecimenDetials_distinct_type_id").then((res) => {
      this.data = res;
      // console.log(this.data,"dsfsdf" )
    });
  },
};
</script>

<style>
.compact-table td {
  padding: 0px 0px !important; /* Reduces cell padding */
}

</style>
