<template>

  <div>
    <div class="text-center text-black text-h6">User Management</div>
    <div class="q-pa-sm q-gutter-sm">
      <q-table title="Treats" :rows="data" :columns="columns" :dense="$q.screen.lt.md" row-key="name" max-width="100%"
        binary-state-sort table-header-style="background-color: #C0C0C0" style="background-color: #F5F5F5"
        class="q-table--dense"  :pagination="pagination">
        <template v-slot:top>

          <div class="q-pa-sm q-gutter-sm">

            <q-dialog v-model="show_dialog">
              <q-card style="width:500px;max-width:500px;background-color: #F5F5F5" text-center>
                <q-card-section>
                  <div class="text-h6 text-center bg-grey-5">User Details</div>
                </q-card-section>

                <!-- add Camra Details Start -->
                <q-card-section>


                  <div class="row ">
                    <q-input v-model="editedItem.id" label="Id:" hidden />
                    <q-input class="fit" outlined  v-model="editedItem.username"  stack-label placeholder="Username"
                      :rules="[val => val && val.length > 0 || 'Please type something']" autofocus dense label="Username"/><q-space />
                    <!-- <q-input outlined  v-model="editedItem.password" placeholder="Password" stack-label
                      :rules="[val => val && val.length > 0 || 'Please type something']"   dense label="Password"/><q-space />

                       -->
                       <q-input class="fit" outlined  v-model="editedItem.password"  stack-label placeholder="please enter password"
                      :rules="[val => val && val.length > 0 || 'Please type something']" autofocus dense label="Password"/><q-space />

                      <q-select  class="fit q-mb-sm"
                        outlined v-model="editedItem.role" input-debounce="0"  use-chips @filter="filterPassage" use-input :options="optionsRole" label="Role:" stack-label dense create /><q-space />

                  </div>
                </q-card-section>
                <!-- add Camra Details END -->

                <q-card-actions align="center">
                  <!-- <q-btn flat label="OK" color="secondary" v-close-popup @click="addRow" ></q-btn> -->
                  <div class="text-center q-mr-xl"><q-btn  dense color="black" v-close-popup
                      label="Cancel"></q-btn></div>
                  <div class="text-center"><q-btn  dense color="black" v-close-popup label="OK"
                      @click="addRow"></q-btn></div>
                </q-card-actions>
              </q-card>
            </q-dialog>
          </div>

        </template>

        <template v-slot:body="props">
          <q-tr :props="props">

            <q-td key="desc" :props="props">
              {{ props.row.username }}
            </q-td>

            <q-td key="password" :props="props">
              {{ props.row.password }}

            </q-td>

            <q-td key="role" :props="props">
              {{ props.row.role}}
            </q-td>



            <q-td key="actions" :props="props">
              <q-btn color="green" label="Edit" @click="editItem(props.row)"  size="11px" class="q-mr-sm"></q-btn>
              <q-btn color="red" label="Delete"  @click="deleteItem(props.row)" size="11px"></q-btn>
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
    <div class="text-center"><q-btn   color="black" label="Add User" @click="addnew" dense></q-btn>
    </div>

  </div>

</template>

<script>
import API from 'src/api'
import { ref } from 'vue'
import { exportFile, useQuasar } from 'quasar'



const columns = [
  {
    name: 'desc',
    required: true,
    label: 'Username',
    align: 'center',
    field: row => row.username,
    format: val => `${val}`,
    sortable: true
  },
  { name: 'password',  align: 'center', label: 'Password', field: 'password', sortable: true },
  { name: 'role', align: 'center', label: 'Role', field: 'role', sortable: true },

  { name: "actions", align: 'center', label: "Actions", field: "actions" }
]

var listLocation=[]
var listRoute=[]

const stringOptionsCam= listLocation
const stringOptionsRoute= listRoute
const stringOptionsRole=  ['user', 'admin' ]



export default {



  setup() {
    const $q = useQuasar()
    const optionsCam = ref(stringOptionsCam)
    const optionsRoute=ref(stringOptionsRoute)
    const optionsRole=ref(stringOptionsRole)

    return {

      pagination: {
            rowsPerPage: 100 // current rows per page being displayed
          },

      listLocation,
      listRoute,

      columns,
      show_dialog: ref(false),
      editedIndex: -1,
      userD: ref(false),
      editedItem: ref({
        id: ref(null),
        username: ref(null),
        password: ref(null),
        role: ref(null),

      }),
      defaultItem: ref({
        id: ref(null),
        username: ref(null),
        password: ref(null),
        role: ref(null),

      }),

      optionsCam,
      optionsRoute,
      optionsRole,

      filterRole(val, update, abort) {
        update(() => {
          const needle = val.toLowerCase()
          optionsRole.value = stringOptionsRole.filter(v => v.toLowerCase().indexOf(needle) > -1)
        })
      }

    }
  },
  components: {},
  methods: {


    async addRow() {

      const id1= this.editedItem.id
      const username1 = this.editedItem.username
      const password1 = this.editedItem.password

      const role1 = this.editedItem.role
      console.log(role1)
      // const role1 = this.editedItem.role.toString()
      // const assignedCamra1 = this.editedItem.assignedCamra.toString()
      // const assignedRoute1 = this.editedItem.assignedRoute.toString()

      // console.log( role1.constructor.name+"mmmmmmm")

      const editedIndex1 = this.editedIndex
      const oldRow = this.data[editedIndex1]
      const updatedRow = this.editedItem

      if (this.editedIndex > -1) {
        if(username1 && password1 && role1 ){
        Object.assign(oldRow, updatedRow) && API("auth.updateUser", { id1: id1, username: username1, password: password1, role:role1 });
        }else {
          this.$q.notify({
            message: 'please Enter all Details.',
            color: 'red',
            icon: 'announcement',
          })}

      } else {
        if (username1 && password1 && role1 ) {

          this.data.push(this.editedItem) && API("auth.createUser", { username: username1, password: password1 , role:role1});
        }
        else {
          this.$q.notify({
            message: 'please Enter all Details.',
            color: 'red',
            icon: 'announcement',
          })
        }
      }
      this.close()




    },

    async deleteItem(item) {
      const id = item.id
      // console.log(id + "oooo")
      const index = this.data.indexOf(item);
      confirm("Are you sure you want to Delete this user?") &&
      this.data.splice(index, 1) && await API('auth.deleteUser', { id });
    },
    async editItem(item) {
      this.editedIndex = this.data.indexOf(item);
      this.editedItem = Object.assign({}, item);
      // this.editedItem = { username: item.username ,role: item.role};

      this.show_dialog = true;
    },
    async addnew() {
      this.show_dialog = true;

    },
    async close() {
      this.show_dialog = false
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      }, 300)
    }
  },

  data: () => ({

    data: []

  }),

  mounted() {
    API('auth.userDetails').then(res => {
      this.data = res
      // console.log(res )
    })





  }

}
</script>

<style lang="sass" >
.q-table--dense
  .q-table
    th
      font-size: 15px
    td
      font-size: 15px
.q-input
  .label
      font-size: 15px



</style>

