import axios from 'axios';

const API_BASE_URL= import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const testMindAPI = {
  /**
   * Send user input to the TestMind backend
   * @param {string} text - The user's input text
   * @returns {Promise<Object>} - The response from the backend
   */
  async sendMessage(text) {
    try {
      const response = await api.post('/api/mind', { text });
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      throw new Error(error.response?.data?.error_message || 'Failed to send message');
    }
  },

  /**
   * Transcribe audio file to text
   * @param {File} audioFile - The audio file to transcribe
   * @returns {Promise<Object>} - The transcription result
   */
  async transcribeAudio(audioFile) {
    try {
      const formData = new FormData();
      formData.append('audio_file', audioFile);
      
      const response = await axios.post(`${API_BASE_URL}/api/transcribe-audio`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      console.error('Audio Transcription Error:', error);
      throw new Error(error.response?.data?.error_message || 'Failed to transcribe audio');
    }
  },

  /**
   * Check if the backend is available
   * @returns {Promise<boolean>} - True if backend is available
   */
  async checkHealth() {
    try {
      await api.get('/api/health');
      return true;
    } catch (error) {
      return false;
    }
  }
};

export default testMindAPI; 