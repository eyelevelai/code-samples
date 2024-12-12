<template>
  <div class="chat-component">
    <MockAPIComponent ref="mockAPI" /> <!-- Include MockApiComponent -->

    <div class="chat-bar">
      <textarea
        v-model="searchQuery"
        :readonly="isSearching || isLoading"
        @keydown.enter.prevent="handleEnterKey"
        @keydown.shift.enter.exact="insertNewLine"
        placeholder="Show me practice problems about 1s, 10s, and 100s."
        rows="1"
        ref="chatBox"
        @input="onInput"
      ></textarea>
    </div>

    <!-- Button container to keep both buttons in the same space -->
    <div class="button-wrapper">
      <!-- Show loading spinner if loading -->
      <div v-if="isLoading" class="no-transition-spinner">
        <CirclesToRhombusesSpinner
          :animation-duration="1200"
          :circles-num="3"
          :circle-size="15"
          color="#A9A9A9"
        />
      </div>

      <!-- Search button -->
      <button v-if="!isSearching && !isLoading" @click="handleEnterKey" class="no-transition">Search</button>

      <!-- Search Again button -->
      <button v-if="isSearching && !isLoading" @click="handleSearchAgain" class="no-transition">Search Again</button>
    </div>
  </div>
</template>

<script>
import { CirclesToRhombusesSpinner } from 'epic-spinners';
import MockAPIComponent from './MockAPIComponent.vue'; // Import MockApiComponent

export default {
  components: {
    CirclesToRhombusesSpinner,
    MockAPIComponent // Register the MockApiComponent
  },
  
  data() {
    return {
      searchQuery: '', // Stores the user's input
      isSearching: false, // Tracks if a search has been triggered
      isLoading: false, // Tracks if the loading spinner is being shown
      hasSearched: false // Tracks if a search was completed before
    };
  },

  methods: {
    // A helper function that returns a promise-based delay
    delay(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },

    async handleEnterKey() {
      if (this.searchQuery.trim() !== '') {

        console.log('searching...')
        this.isLoading = true; // Show the loading spinner
        this.hasSearched = true; // Mark that a search has been triggered

        try {
          // Simulate a loading delay
          await this.delay(3000);

          // Get reference to the mock API component
          const mockAPI = this.$refs.mockAPI;
          const response = mockAPI.findResponse(this.searchQuery); // Get the mock response

          console.log('search complete')
          console.log(response)

          this.isLoading = false; // Hide the loading spinner
          this.isSearching = true; // Show the "Search Again" button

          // Emit the search event with the response data
          if (response) {
            this.$emit('search', response); // Emit the array of responses
          } else {
            console.log('No response found');
            this.$emit('search', []); // Emit an empty array if no match is found
          }
        } catch (error) {
          console.error('Error during search:', error);
          this.isLoading = false;
        }
      }
    },

    handleSearchAgain() {
      this.resetSearch(); // Reset the search component
      this.$emit('clear'); // Emit an event to the parent to clear the search result
    },

    insertNewLine() {
      const textarea = this.$refs.chatBox;
      const cursorPosition = textarea.selectionStart;
      this.searchQuery =
        this.searchQuery.slice(0, cursorPosition) +
        '\n' +
        this.searchQuery.slice(cursorPosition);
      this.$nextTick(() => {
        textarea.selectionStart = cursorPosition + 1;
        textarea.selectionEnd = cursorPosition + 1;
      });
    },

    onInput() {
      this.autoResize();
    },

    autoResize() {
      const textarea = this.$refs.chatBox;
      textarea.style.height = 'auto'; // Reset height to auto to calculate the correct height
      textarea.style.height = textarea.scrollHeight + 'px'; // Set height to match scrollHeight
    },

    resetSearch() {
      // Reset the component to its initial state
      this.searchQuery = ''; // Clear the input
      this.isSearching = false; // Show the "Search" button
      this.hasSearched = false; // Reset search state
      this.autoResize(); // Ensure proper resizing
    }
  },

  mounted() {
    this.autoResize();
  }
};
</script>

<style scoped>
.chat-component {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
}

.chat-bar textarea {
  width: 600px;
  padding: 12px 8px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  resize: none;
  overflow: hidden;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  min-height: 40px;
  line-height: 1.5;
  box-sizing: border-box;
}

.chat-bar textarea:focus {
  outline: none;
}

.button-wrapper {
  position: relative;
  width: 140px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

button {
  width: 100%;
  padding: 8px 16px;
  font-size: 16px;
  cursor: pointer;
}

.no-transition {
  transition: none !important;
}

.no-transition-spinner {
  animation: none !important;
}
</style>
