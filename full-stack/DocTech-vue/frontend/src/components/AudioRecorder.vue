<template>
  <div class="audio-recorder">
    <button @click="toggleRecording" class="recording-button">
      {{ isRecording ? "Stop Recording" : "Start Recording" }}
    </button>
    <canvas ref="canvas" width="200" height="200"></canvas> <!-- Smaller canvas -->
    <audio ref="audio" :src="audioResponseUrl" type="audio/mpeg" style="display: none;"></audio>
  </div>
</template>

<script>
export default {
  name: "AudioRecorder",
  data() {
    return {
      isRecording: false,
      mediaRecorder: null,
      audioChunks: [],
      audioResponseUrl: null,
      plan: null,
      microphoneStream: null,
      audioContext: null,
      analyser: null,
      animationFrameId: null,
      silenceTimeout: null,
      silenceThreshold: 0.05, // Adjust this threshold as needed
    };
  },
  methods: {
    async toggleRecording() {
      if (this.isRecording) {
        this.stopRecording();
      } else {
        await this.startRecording();
      }
    },
    async startRecording() {
      this.isRecording = true;
      this.audioChunks = [];
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.microphoneStream = stream;

      this.mediaRecorder = new MediaRecorder(stream);
      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) this.audioChunks.push(event.data);
      };
      this.mediaRecorder.onstop = this.onRecordingStop;
      this.mediaRecorder.start();

      this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const source = this.audioContext.createMediaStreamSource(stream);
      this.analyser = this.audioContext.createAnalyser();
      this.analyser.fftSize = 256;
      source.connect(this.analyser);

      this.startVisualizing();
    },
    stopRecording() {
      this.isRecording = false;
      this.mediaRecorder.stop();
      this.microphoneStream.getTracks().forEach((track) => track.stop());
      if (this.silenceTimeout) clearTimeout(this.silenceTimeout);
      cancelAnimationFrame(this.animationFrameId);
    },
    async onRecordingStop() {
      const audioBlob = new Blob(this.audioChunks, { type: "audio/ogg; codecs=opus" });
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.ogg");

      try {
        console.log("Sending request to /decide_and_respond...");
        const response = await fetch("http://localhost:5000/decide_and_respond", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();

        console.log("Response from /decide_and_respond:", data);

        this.audioResponseUrl = data.audio_url;
        this.plan = data.plan;

        // Ensure the audio source is loaded, then play it
        this.$nextTick(async () => {
          try {
            await this.$refs.audio.load();  // Wait for the audio to load
            await this.$refs.audio.play();  // Wait for the audio to start playing
          } catch (error) {
            console.error("Error playing audio:", error);
          }
        });

        // Execute the plan in parallel with the audio playback
        this.executePlan();
      } catch (error) {
        console.error("Error handling audio file:", error);
      }
    },
    executePlan() {
      if (this.plan) {
        console.log("Sending plan to /execute_plan:", this.plan);

        fetch("http://localhost:5000/execute_plan", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.plan),
        })
        .then(response => response.json())
        .then(data => {
          console.log("Response from /execute_plan:", data);
          this.$emit("api-response", data);  // Emit the response for any parent components

          // If follow-up audio is provided, play it after executing the plan
          if (data.followup_audio_url) {
            this.$nextTick(async () => {
              try {
                this.audioResponseUrl = data.followup_audio_url;
                await this.$refs.audio.load();  // Load the new follow-up audio
                await this.$refs.audio.play();  // Play the follow-up audio
              } catch (error) {
                console.error("Error playing follow-up audio:", error);
              }
            });
          }
        })
        .catch(error => console.error("Error executing plan:", error));
      }
    },
    startVisualizing() {
      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext("2d");
      const bufferLength = this.analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const draw = () => {
        this.analyser.getByteFrequencyData(dataArray);

        let sumSquares = 0.0;
        for (let i = 0; i < bufferLength; i++) {
          sumSquares += (dataArray[i] / 255) ** 2;
        }
        const rms = Math.sqrt(sumSquares / bufferLength); // Root Mean Square for volume level
        const radius = this.isRecording ? rms * 100 : 10;
        const color = this.isRecording ? "rgba(0, 150, 255, 0.8)" : "rgba(200, 200, 200, 0.2)";

        ctx.fillStyle = "black";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.beginPath();
        ctx.arc(canvas.width / 2, canvas.height / 2, radius, 0, 2 * Math.PI);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.closePath();

        // Auto-stop recording if volume is below threshold
        if (this.isRecording && rms < this.silenceThreshold) {
          if (!this.silenceTimeout) {
            this.silenceTimeout = setTimeout(() => {
              this.stopRecording();
            }, 1000); // Silence period before stopping, adjust as needed
          }
        } else {
          clearTimeout(this.silenceTimeout);
          this.silenceTimeout = null;
        }

        this.animationFrameId = requestAnimationFrame(draw);
      };

      draw();
    },
  },
  beforeUnmount() {
    cancelAnimationFrame(this.animationFrameId);
    if (this.silenceTimeout) clearTimeout(this.silenceTimeout);
    if (this.audioContext) this.audioContext.close();
    if (this.microphoneStream) {
      this.microphoneStream.getTracks().forEach((track) => track.stop());
    }
  },
};
</script>

<style scoped>
.audio-recorder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

canvas {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background-color: black;
  box-shadow: 0 0 20px rgba(0, 150, 255, 0.6);
}

.recording-button {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: bold;
  color: white;
  background-color: #0077cc;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 20px;
  margin-bottom: 20px;
}

.recording-button:hover {
  background-color: #005fa3;
}

.recording-button:active {
  background-color: #00487a;
}
</style>
