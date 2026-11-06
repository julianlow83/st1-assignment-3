from __future__ import annotations
from typing import Optional, List, Tuple
from datetime import datetime
from .domain import Appointment, AppointmentStatus

def appointment_sort_key(appointment: Appointment) -> Tuple[datetime, str]:
    """
    Pure sorting key extractor.
    Extracts (date_time, appointment_id) without side effects or mutations.
    """
    return appointment.date_time, appointment.appointment_id

def select_appointments(
    appointments: List[Appointment],
    practitioner_id: str,
    status: Optional[AppointmentStatus] = None
) -> List[Appointment]:
    """
    Pure query. Filters by practitioner ID and optional status enum;
    returns a new list sorted ascending by date/time and tie-broken by ID.
    Does not mutate the input list or contained appointment objects.
    """
    filtered = [
        appt for appt in appointments
        if appt.practitioner.practitioner_id == practitioner_id
        and (status is None or appt.status == status)
    ]
    return sorted(filtered, key=appointment_sort_key)