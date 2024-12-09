<template>
    <div>
      <iframe v-if="currentPdfUrl" :src="iframeSrc" class="pdf-iframe"></iframe>
      <div v-else class="no-pdf">Ask A Question!</div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      apiResponse: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        currentPdfUrl: null,
        currentPage: 1,
      };
    },
    computed: {
      iframeSrc() {
        if (this.currentPdfUrl) {
          return `${this.currentPdfUrl}#page=${this.currentPage}`;
        }
        return '';
      },
    },
    watch: {
      apiResponse: {
        immediate: true,
        handler(newVal) {
          this.handleApiResponse(newVal);
        },
      },
    },
    methods: {
      handleApiResponse(response) {
        if (response.non_determ) {
          // Could not determine action; do nothing or show an error
          console.error('Could not determine action from API response.');
          return;
        }
  
        if (response.pdf) {
          // New PDF URL provided
          this.currentPdfUrl = response.pdf;
          this.currentPage = response.page || 1;
        } else if (this.currentPdfUrl) {
          // No new PDF URL; handle relative navigation
          if (response.next_page) {
            this.currentPage += 1;
          }
          if (response.previous_page) {
            this.currentPage = Math.max(this.currentPage - 1, 1);
          }
          if (response.scroll_up) {
            this.currentPage = Math.max(this.currentPage - 1, 1);
          }
          if (response.scroll_down) {
            this.currentPage += 1;
          }
          if (response.snap_page && response.page) {
            this.currentPage = response.page;
          }
        } else {
          // No current PDF URL and no new URL provided
          console.warn('No PDF URL available to navigate.');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .pdf-iframe {
    width: 100%;
    height: 100vh;
    border: none;
  }
  
  .no-pdf {
    text-align: center;
    margin-top: 20px;
    color: #666;
  }
  </style>
  