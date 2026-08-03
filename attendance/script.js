// Web App Deployment Endpoint
const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxwqoOye-M2llgR4hso3Z71EkoAwcCiTRo6CPqjVbdjCTo2exHA-bNa4CpkA7ReA5lFUg/exec";

let configData = {};

const dateSelect = document.getElementById('classDate');
const groupSelect = document.getElementById('groupName');
const previewImg = document.getElementById('previewImg');
const previewPlaceholder = document.getElementById('previewPlaceholder');
const attendanceForm = document.getElementById('attendanceForm');
const submitBtn = document.getElementById('submitBtn');
const statusMessage = document.getElementById('statusMessage');

// Fetch Config Data on Page Load
async function loadConfig() {
  try {
    const response = await fetch(SCRIPT_URL);
    const json = await response.json();

    if (json.status === "success" && json.data) {
      configData = json.data;
      populateDates();
    } else {
      showStatus("Failed to load options from server.", "error");
    }
  } catch (err) {
    showStatus("Network error while loading configuration.", "error");
  }
}

// Populate Date Dropdown
function populateDates() {
  dateSelect.innerHTML = '<option value="">-- Select Date --</option>';
  const dates = Object.keys(configData);

  if (dates.length === 0) {
    dateSelect.innerHTML = '<option value="">No dates available</option>';
    return;
  }

  dates.forEach(date => {
    const opt = document.createElement('option');
    opt.value = date;
    opt.textContent = date.replace(/_/g, '/');
    dateSelect.appendChild(opt);
  });
}

// Handle Date Selection Change
dateSelect.addEventListener('change', () => {
  const selectedDate = dateSelect.value;
  groupSelect.innerHTML = '<option value="">-- Select Group --</option>';
  resetPreview();

  if (selectedDate && configData[selectedDate]) {
    groupSelect.disabled = false;
    configData[selectedDate].forEach(item => {
      const opt = document.createElement('option');
      opt.value = item.group;
      opt.textContent = item.group;
      groupSelect.appendChild(opt);
    });
  } else {
    groupSelect.disabled = true;
    groupSelect.innerHTML = '<option value="">Select Date First</option>';
  }
});

// Handle Group Selection Change -> Update Image
groupSelect.addEventListener('change', updateImagePreview);

function updateImagePreview() {
  const selectedDate = dateSelect.value;
  const selectedGroup = groupSelect.value;

  if (selectedDate && selectedGroup && configData[selectedDate]) {
    const match = configData[selectedDate].find(item => item.group === selectedGroup);
    if (match && match.imageUrl) {
      previewImg.src = match.imageUrl;
      previewImg.style.display = 'block';
      previewPlaceholder.style.display = 'none';
      return;
    }
  }
  resetPreview();
}

function resetPreview() {
  previewImg.src = '';
  previewImg.style.display = 'none';
  previewPlaceholder.style.display = 'block';
}

// Handle Form Submission
attendanceForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  submitBtn.disabled = true;
  submitBtn.textContent = 'Submitting...';
  hideStatus();

  const payload = {
    date: dateSelect.value,
    group: groupSelect.value,
    email: document.getElementById('email').value.trim(),
    rollNumber: document.getElementById('rollNumber').value.trim(),
    serialNumber: document.getElementById('serialNumber').value.trim()
  };

  try {
    // Send data as raw text to avoid pre-flight CORS issues with Google Apps Script
    const response = await fetch(SCRIPT_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (result.status === 'success') {
      showStatus('✅ ' + result.message, 'success');
      document.getElementById('serialNumber').value = '';
    } else if (result.status === 'conflict') {
      showStatus('⚠️ ' + result.message, 'warning');
    } else {
      showStatus('❌ ' + (result.message || 'An error occurred.'), 'error');
    }
  } catch (err) {
    showStatus('❌ Submission failed. Please try again.', 'error');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Submit Attendance';
  }
});

function showStatus(text, type) {
  statusMessage.textContent = text;
  statusMessage.className = `status-msg ${type}`;
  statusMessage.style.display = 'block';
}

function hideStatus() {
  statusMessage.style.display = 'none';
}

// Initialize Page
loadConfig();