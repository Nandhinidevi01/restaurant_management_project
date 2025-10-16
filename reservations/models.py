from django.db import models
from django .utils import timezone
from datetime import timedelta, datetime
from reservations.models import Reservation


class Reservation(moodels.Model):
    customer_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.customer_name} ({self.start_time} - {self.end_time})"

    @classmethod
    def find_available_slots(cls, start_range, end_range, slot_duration=timedelta(hours=1)):
        """
        Finds available time slots within a given date/time range.

        Parameters:
        - start_range (datetime): The starting datetime of the search range.
        - end_range (datetime): The ending datetime of the search range.
        - slot duration (timedelta): Duration of each slot (default 1 hour).

        Returns:
        - A list of tuples (slot_start, slot_end) representing available time slots.
        """

        # Fetch all reservations that overlop with the given range
        overlapping_reservations = cls.objects.filter(
            start_time__lt=end_range,
            end_time__gt=start_range
        ).order_by('start_time')

        # Initialize the list of available slots
        available_slots = []

        current_start = start_range

        for reservation in overlapping_reservations:
            # if there's gap before the reservation starts
            if reservation.start_time > current_start:
                slot_end = min(reservation.start_time, end_range)
                while current_start + slot_duration <= slot_end:
                    available_slots.append((current_start, current_start + slot_duration))
                    current_start += slot_duration

            if reservation.end_time > current_start:
                current_start = reservation.end_time

        #After the last reservation, chech remaining time
        while current_start + slot_duration <= end_range:
            available_slots.append((current_start, current_start + slot_duration))
            current_start += slot_duration
        return available_slots

start_range = datetime(2025, 10, 17, 9, 0)
end_range = datetime(2025, 10, 17, 18, 0)

available = Reservation.find_available_slots(start_range, end_range, timedelta(hours=1))

for slot in available:
    print(f"Available: {slot[0].strftime('%H:%M')} - {slot[1].strftime('%H:%M')}")