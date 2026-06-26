<template>

      <div class="q-mb-lg ">
      <q-card-section class="row ">
          <q-space/>
          <q-btn icon="close"  round dense v-close-popup />
        </q-card-section>
      </div>



    <q-uploader
    class="full-width"
      ref="uploader"
      color="amber"
      text-color="black"
      label="Select files to upload"
      @added="onFilesAdded"
      no-thumbnails
      multiple
    >

    <template v-slot:list="scope">

        <q-list separator>

          <q-item v-for="file in scope.files" :key="file.__key">
            <q-item-section>
              <q-item-label class="full-width ellipsis">
                {{ file.name }}
              </q-item-label>
<!--
              <q-item-label caption>
                Status: {{ file.__status }}
              </q-item-label> -->

              <q-item-label caption>
                <!-- {{ file.__sizeLabel }} / {{ file.__progressLabel }} -->
                {{ file.__sizeLabel }}
              </q-item-label>
            </q-item-section>

            <q-item-section
              v-if="file.__img"
              thumbnail
              class="gt-xs"
            >
              <img :src="file.__img.src">
            </q-item-section>

            <q-item-section top side >
              <q-btn
                class="gt-xs"
                size="12px"
                flat
                dense
                round
                icon="delete"
                @click="scope.removeFile(file)"
              />
            </q-item-section>
          </q-item>

        </q-list>



      </template>


  </q-uploader>
    <div class="row text-center" >
      <q-btn class="q-mt-lg "   :color="uploadBtnColor"  label="Upload Data" @click="uploadFiles" :disable="uploadDisabled || uploading" />
      <q-spinner v-if="uploading" color="primary" size="50px" />

    </div>
    <div class="row justify-center" v-if="uploadMessage">{{ uploadMessage }}</div>



<q-space />




</template>




<script>
  import API from 'src/api'
  import { ref } from 'vue'
  import { exportFile, useQuasar } from 'quasar'
  import uploadbtn from 'src/components/user/uploadbtn';


export default {
  components: {},

  // comming form uploadImgActivity.vue
  props: {
    passUuid:String,
    },
  data() {

    return {

      selectedFiles: [],
      uploading: false,
      uploadDisabled: true,
      uploadMessage: "", // Added a new data property to hold the upload message
      fileUrls: [],
      processingdone:false,
    };
  },
  mounted(){

  },
  computed:{
    uploadBtnColor() {
      return this.selectedFiles.length > 0 ? 'green' : 'red';
    }
  },
  methods: {

     call_serverfunction_processfbulk(){

          const allfilesname = this.fileUrls.map(file => file.url)
          const randomid=this.passUuid;
          API('home.processFilesbulk',{files:allfilesname,randomid: randomid} ).then(res => {
          console.log(res,"server funcation call");
        })
    },

    addFiles() {
  try {
    const a = this.fileUrls;
    a.forEach((experiment) => {
      const {
        url,
        mimetype,
        size,
        headers,

      } = experiment;

      const file_meta = JSON.stringify(headers);
      // Make the API call with the extracted values
      API("auth.createFilebulk", {
        experiment_id:this.passUuid,
        file_addr:url,
        file_type:mimetype,
        file_size:size.toString(),
        file_meta
      });
    });

    // If the loop completes without errors, show the notification
    this.$q.notify({
      message: 'Files Uploaded',
      color: 'green', // You can change the color to indicate success
      icon: 'announcement',
    });
    // Call server function to process
    this.call_serverfunction_processfbulk();

  } catch (error) {
    // If an error occurs, you can handle it here
    console.error('Error in addcheck:', error);

    this.$q.notify({
      message: 'Error occurred while saving Files',
      color: 'red',
      icon: 'announcement',
    });
  }
},
    onFilesAdded(files) {
      this.selectedFiles = files;
      this.uploadDisabled = files.length === 0;
    },
    uploadFiles() {
  if (!this.selectedFiles.length) return;

  this.uploading = true;
  const formData = new FormData();

  for (let i = 0; i < this.selectedFiles.length; i++) {
    formData.append('files', this.selectedFiles[i]);
  }
 // Dynamically detect the upload URL
 const UPLOAD_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:7070/upload'  // Localhost for development
    : `http://${window.location.hostname}:7070/upload`;  // Dynamic IP in production

  fetch(UPLOAD_URL, {
    method: 'POST',
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Failed to upload files.');
      }
      return response.json();
    })
    .then((data) => {
      // console.log(data.message);

      // Store the file URLs in the data property
      // this.fileUrls = data.files.map((file) => file.url);
      this.fileUrls = data.files;
      this.uploadMessage = "Upload Next: All will be process on server!";
      this.uploading = false;
      this.addFiles();

      setTimeout(() => {
        this.$emit('close-dialog');
      }, 1000);


    })
    .catch((error) => {
      console.error('Error uploading files:', error);
      this.uploadMessage = "Error uploading files. Please try again.";
      this.uploading = false;
    });
},

  },
};
</script>

<style>
/* Add your custom styles here */
</style>
