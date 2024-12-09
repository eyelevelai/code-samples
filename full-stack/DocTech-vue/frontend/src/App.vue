<!-- App.vue -->
<template>
  <div class="app-container">
    <div class="recorder-container">
      <AudioRecorder @api-response="handleApiResponse" />
    </div>
    <div class="pdf-viewer-container">
      <PdfViewer :apiResponse="apiResponse" />
    </div>
  </div>
</template>

<script>
import PdfViewer from './components/PdfViewer.vue';
import AudioRecorder from './components/AudioRecorder.vue';

export default {
  components: {
    PdfViewer,
    AudioRecorder,
  },
  data() {
    return {
      apiResponse: {},
    };
  },
  methods: {
    handleApiResponse(response) {
      this.apiResponse = response;
    },
  },
};
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  min-height: 100vh;
  padding: 20px;
  background-color: #f0f4f8;
}

.recorder-container {
  margin-bottom: 20px;
}

.pdf-viewer-container {
  width: 80vw;
  height: 60vh;
  border: 1px solid #ddd;
  background-color: white;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}
</style>
