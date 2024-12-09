<template>
  <div class="example-component">
    <!-- Description text -->
    <p v-if="description">{{ description }}</p>

    <!-- Embed the PDF in an iframe and display the first page -->
    <iframe :src="pdfIframeUrl" frameborder="0" class="pdf-iframe"></iframe>
  
    <!-- Buttons for opening the PDF and exploring -->
    <div class="button-container">
      <button @click="openPdf" class="open-button">Open PDF</button>
      <button @click="explore" class="open-button" v-if="exploreUrl">Explore</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    pdfUrl: {
      type: String,
      required: true, // URL of the PDF file
    },
    description: {
      type: String,
      required: true
    },
    exploreUrl: {
      type: String,
      required: false
    }
  },
  computed: {
    pdfIframeUrl() {
      // Use PDF URL for the iframe
      return this.pdfUrl;
    },
  },
  methods: {
    // Open the PDF in a new tab
    openPdf() {
      window.open(this.pdfUrl, "_blank");
    },
    explore() {
      window.open(this.exploreUrl, "_blank");
    },
  },
};
</script>

<style scoped>
.example-component {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 20px; /* Add spacing between elements */
  padding: 20px;
  background-color: #171717;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.pdf-iframe {
  width: 100%;
  max-width: 600px;
  height: 400px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

p {
  margin: 0;
  padding: 0;
  font-size: 16px;
  color: #d8d8d8;
  text-align: center;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 15px; /* Add space between buttons */
  width: 100%;
}

.open-button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #111111; /* Light gray background */
  color: #878787; /* Darker text */
  /* border: 1px solid #ccc; */
  border-radius: 5px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.open-button:hover {
  background-color: #595959; /* Darker gray on hover */
  color: #ffffff;
  border: 1px solid #595959;
}
</style>
