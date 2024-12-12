<template>
    <div class="logo-container">
      <img src="../assets/core_explorer_transparent.png" alt="Core Explorer Logo" class="logo-image" />
      <p class="logo-text"><b>Core Explorer</b></p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LogoComponent'
  }
  </script>
  
  <style scoped>
  .logo-container {
    display: flex;
    flex-direction: column;
    align-items: center; /* Horizontally center the logo and text */
    margin-bottom: 20px; /* Reduced space below the logo to the next component */
  }
  
  .logo-image {
    width: 100px; /* Fixed size for the logo */
    height: auto; /* Maintain aspect ratio */
    border-radius: 50%; /* Make the image circular */
    mask-image: radial-gradient(circle, rgba(255,255,255,1) 60%, rgba(255,255,255,0) 100%); /* Radial transparency fade */
    margin-bottom: -30px;
  }
  
  .logo-text {
    margin-top: 5px; /* Reduce the space between the logo and the text */
    margin-bottom: 0; /* No extra space below the text */
  }
  </style>
  