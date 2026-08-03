// Web App Deployment Endpoint
const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxwqoOye-M2llgR4hso3Z71EkoAwcCiTRo6CPqjVbdjCTo2exHA-bNa4CpkA7ReA5lFUg/exec";

let configData = {};
let isZoomed = false;

const dateSelect = document.getElementById('classDate');
const groupSelect = document.getElementById('groupName');
const previewImg = document.getElementById('previewImg');
const previewPlaceholder = document.getElementById('previewPlaceholder');
const attendanceForm = document.getElementById('attendanceForm');
const submitBtn = document.getElementById('submitBtn');
const statusMessage = document.getElementById('statusMessage');

// Loading Modal Elements
const loadingModal = document.getElementById('loadingModal');
const loadingText = document.getElementById('loadingText');

// Image Lightbox Elements
const imageModal = document.getElementById('imageModal');
const fullscreenImg = document.getElementById('fullscreenImg');
const closeImageModal = document.getElementById('closeImageModal');

// Help Box Elements
const helpToggleBtn = document.getElementById('helpToggleBtn');
const helpBox = document.getElementById('helpBox');
const closeHelpBtn = document.getElementById('closeHelpBtn');

// Toggle Help Box
helpToggleBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  helpBox.classList.toggle('active');
});

closeHelpBtn.addEventListener('click', () => {
  helpBox.classList.remove('active');
});

// Close Help Box when clicking outside
document.addEventListener('click', (e) => {
  if (!helpBox.contains(e.target) && e.target !== helpToggleBtn) {
    helpBox.classList.remove('active');
  }
});

function showModal(text = "Processing request...") {
  loadingText.textContent = text;
  loadingModal.classList.add('active');
}

function hideModal() {
  loadingModal.classList.remove('active');
}

// Fetch Config Data on Page Load
async function loadConfig() {
  showModal("Please wait. Loading options...");
  try {
    const response = await fetch(SCRIPT_URL);
    const json = await response.json();

    if (json.status === "success" && json.data) {
      configData = json.data;
      populateDates();
    } else {
      showStatus("Failed to load options from server. Try later...", "error");
    }
  } catch (err) {
    showStatus("Network error while loading configuration.", "error");
  } finally {
    hideModal();
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

// Fullscreen Image & Zoom Handlers
previewImg.addEventListener('click', () => {
  if (previewImg.src) {
    fullscreenImg.src = previewImg.src;
    imageModal.classList.add('active');
  }
});

// Click image to toggle zoom
fullscreenImg.addEventListener('click', (e) => {
  e.stopPropagation(); // Prevents background click from closing modal
  isZoomed = !isZoomed;

  if (isZoomed) {
    fullscreenImg.classList.add('zoomed');
    updateZoomPosition(e);
  } else {
    resetZoom();
  }
});

// Pan zoomed image following cursor position
fullscreenImg.addEventListener('mousemove', (e) => {
  if (isZoomed) {
    updateZoomPosition(e);
  }
});

function updateZoomPosition(e) {
  const rect = fullscreenImg.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 100;
  const y = ((e.clientY - rect.top) / rect.height) * 100;
  fullscreenImg.style.transformOrigin = `${x}% ${y}%`;
}

function resetZoom() {
  isZoomed = false;
  fullscreenImg.classList.remove('zoomed');
  fullscreenImg.style.transformOrigin = 'center center';
}

function closeFullscreen() {
  resetZoom();
  imageModal.classList.remove('active');
}

closeImageModal.addEventListener('click', closeFullscreen);

imageModal.addEventListener('click', (e) => {
  if (e.target === imageModal) {
    closeFullscreen();
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    if (imageModal.classList.contains('active')) closeFullscreen();
    if (helpBox.classList.contains('active')) helpBox.classList.remove('active');
  }
});

// Handle Form Submission
attendanceForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  submitBtn.disabled = true;
  hideStatus();
  showModal("Submitting attendance...");

  const payload = {
    date: dateSelect.value,
    group: groupSelect.value,
    email: document.getElementById('email').value.trim(),
    rollNumber: document.getElementById('rollNumber').value.trim(),
    serialNumber: document.getElementById('serialNumber').value.trim()
  };

  try {
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
    hideModal();
    submitBtn.disabled = false;
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