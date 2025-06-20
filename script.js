form.addEventListener('submit', function (e) {
  e.preventDefault();

  const name = document.getElementById('name').value;
  const doctor = document.getElementById('doctor').value;
  const time = document.getElementById('time').value;
  const duration = document.getElementById('duration').value;

  fetch('/book', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name, doctor, time, duration })
  })
  .then(res => res.json())
  .then(data => {
    tableBody.innerHTML = ''; // Clear old table
    data.forEach(row => {
      const newRow = document.createElement('tr');
      newRow.innerHTML = `<td>${row.Patient_ID}</td><td>${doctor}</td><td>${row.Scheduled_Time}</td><td>${duration} min</td>`;
      tableBody.appendChild(newRow);
    });
    form.reset();
  });
});
