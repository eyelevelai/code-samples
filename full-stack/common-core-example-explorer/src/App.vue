<template>
  <div>
    <!-- Add the Logo Component here -->
    <LogoComponent />

    <!-- Pass the handleSearch method as a listener for the search event -->
    <ChatComponent @search="handleSearch" @clear="clearSearch" />

    <!-- Wrap the ExampleListComponent in a transition to expand and fade in/out -->
    <transition
      name="expand-fade"
      mode="out-in"
      @before-enter="beforeEnter"
      @enter="enter"
      @leave="leave"
    >
      <!-- Only render the ExampleListComponent if there are pdfs -->
      <div v-if="pdfs.length" class="example-list-wrapper">
        <ExampleListComponent :pdfList="pdfs" />
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'; // Import Vue's ref for reactive data
import ChatComponent from "./components/ChatComponent.vue";
import ExampleListComponent from './components/ExampleListComponent.vue';
import LogoComponent from './components/LogoComponent.vue'; // Import the logo component

// Reactive reference to store the PDFs returned from the API response
const pdfs = ref([]);

// Function to handle the search event and update the pdfs list
function handleSearch(response) {
  pdfs.value = response; // Update the list with the API response
}

// Function to clear the search results
function clearSearch() {
  pdfs.value = []; // Clear the list of PDFs
}

// Transition hooks for animating height and opacity
function beforeEnter(el: HTMLElement) {
  el.style.height = '0';
  el.style.opacity = '0';
}

function enter(el: HTMLElement) {
  const height = el.scrollHeight; // Get the full height of the element
  el.style.transition = 'height 0.5s ease, opacity 0.5s ease';
  el.style.height = `${height}px`;
  el.style.opacity = '1';
}

function leave(el: HTMLElement) {
  el.style.transition = 'height 0.5s ease, opacity 0.5s ease';
  el.style.height = '0';
  el.style.opacity = '0';
}
</script>
