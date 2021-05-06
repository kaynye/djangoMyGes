document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        timeZone: 'Europe/Paris',
        locales: "fr",
        hiddenDays: [0],
        businessHours: {
            daysOfWeek: [1, 2, 3, 4 , 5, 6],
            startTime: '07:00', 
            endTime: '22:00',
        },
        eventSources: [
            {
                url: '/get_events',
                method: 'POST',
                success: function(response) {
                    console.log(response)
                }
            }
        ]
    });
    calendar.render();
});