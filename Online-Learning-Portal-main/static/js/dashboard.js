const starContainers = [document.querySelectorAll('.stars span'), document.querySelectorAll('.stars1 span'), document.querySelectorAll('.stars2 span')];

starContainers.forEach((container) => {
  container.forEach((star, index) => {
    star.addEventListener('click', () => {
      container.forEach((s, i) => {
        s.classList.toggle('active', i <= index);
      });
    });
  });
});

const openBookingModal = document.getElementById('openBookingModal');
const bookingModal = document.getElementById('bookingModal');
const closeModal = document.getElementById('closeModal');
const cancelBooking = document.getElementById('cancelBooking');
const bookingForm = document.getElementById('bookingForm');
const bookingStatus = document.getElementById('booking-status');

openBookingModal.addEventListener('click', () => {
  bookingModal.style.display = 'block';
});

closeModal.addEventListener('click', () => {
  bookingModal.style.display = 'none';
});

window.addEventListener('click', (event) => {
  if (event.target === bookingModal) {
    bookingModal.style.display = 'none';
  }
});

cancelBooking.addEventListener('click', () => {
  bookingModal.style.display = 'none';
});

bookingForm.addEventListener('submit', (event) => {
  event.preventDefault();

  const course = document.getElementById('course').value;
  const trainee = document.getElementById('trainee').value;
  const date = document.getElementById('date').value;
  const slot = document.getElementById('slot').value;

  if (!course || !trainee || !date || !slot) {
    alert('Please fill in all fields.');
    return;
  }

  fetch('/get_bookings')
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        bookingStatus.innerHTML = `<p>${data.error}</p>`;
        return;
      }

      bookingStatus.innerHTML = '';

      data.bookings.forEach(booking => {
        const bookingDiv = document.createElement("div");
        bookingDiv.className = "booking-card";

        bookingDiv.innerHTML = `
          <h3 class="course-name">${booking.course}</h3>
          <p class="trainee-name">Trainee: ${booking.trainee}</p>
          <p class="booking-info">
            <span class="booking-date">${booking.booking_date}</span>
            <span class="booking-slot">${booking.slot}</span>
          </p>
          <button class="edit-button" onclick="editBooking(${booking.id})">Edit</button>
        `;

        bookingStatus.appendChild(bookingDiv);
      });
    })
    .catch(error => {
      bookingStatus.innerHTML = `<p>An error occurred: ${error}</p>`;
    });
    bookingModal.style.display = 'none';

  fetch('/book', {
    method: 'POST',
    body: new FormData(bookingForm)
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      bookingStatus.textContent = `You have booked: ${course} for ${trainee} on ${date} at ${slot}`;
      bookingModal.style.display = 'none'; 
    } else {
      alert('Booking failed: ' + data.message);
    }
  })
});

function editBooking(bookingId) {
  alert(`Edit booking with ID: ${bookingId}`);
}
