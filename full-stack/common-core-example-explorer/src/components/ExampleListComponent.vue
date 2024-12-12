<template>
    <div class="example-list">
      <!-- Iterate over the list of PDFs and render ExampleComponent for each item -->
      <div v-for="(item, index) in pdfList" :key="index" class="example-item">
        <ExampleComponent :pdfUrl="item.pdfUrl" :description="item.description" :exploreUrl="item.exploreUrl" />
      </div>
    </div>
  </template>
  
  <script>
  import ExampleComponent from './ExampleComponent.vue';
  
  export default {
    components: {
      ExampleComponent
    },
    props: {
      pdfList: {
        type: Array,
        required: true
      }
    }
  };
  </script>
  
  <style scoped>
  .example-list {
    display: flex;
    justify-content: space-between; /* Space items evenly */
    align-items: flex-end; /* Align all items by their bottom */
    gap: 20px; /* Add space between items */
  }
  
  .example-item {
    flex: 1 1 300px; /* Flexible width, min-width of 300px */
    display: flex;
    flex-direction: column;
  }
  </style>