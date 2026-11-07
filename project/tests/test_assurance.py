"""Stage 11 Responsible AI Assurance Tests for SmartCare."""

import pytest
from datetime import datetime
from smartcare.data_store import SmartCareDataStore
from smartcare.services import PatientService, PractitionerService, AppointmentService
from smartcare.domain import AppointmentStatus


def test_assurance_patient_lookup_error_sanitization():
    """Verify malformed input strings and blank IDs correctly raise ValueError without leaking tracebacks."""
    store = SmartCareDataStore()
    patient_svc = PatientService(store)

    with pytest.raises(ValueError):
        patient_svc.find_patient("   ")
    with pytest.raises(ValueError):
        patient_svc.find_patient("")


def test_assurance_rescheduling_conflict_and_history_retention():
    """Verify failed rescheduling attempts due to practitioner conflicts leave original state unmutated."""
    store = SmartCareDataStore()
    patient_svc = PatientService(store)
    practitioner_svc = PractitionerService(store)
    appointment_svc = AppointmentService(store)

    patient_svc.register_patient("P101", "Alice Smith")
    patient_svc.register_patient("P102", "Bob Jones")
    practitioner_svc.register_practitioner("D201", "Dr. John Doe", "General Practice")

    t1 = datetime(2026, 11, 1, 10, 0)
    t2 = datetime(2026, 11, 1, 11, 0)

    appt1 = appointment_svc.book_appointment("A301", "P101", "D201", t1)
    appointment_svc.book_appointment("A302", "P102", "D201", t2)

    # Attempt conflicting reschedule from t1 to t2 where D201 is already booked
    with pytest.raises(ValueError):
        appointment_svc.reschedule_appointment("A301", t2)

    # Assert strict non-mutation of original appointment time
    assert appt1.date_time == t1
    assert appt1.status is AppointmentStatus.SCHEDULED
    assert store.find_appointment("A301").date_time == t1