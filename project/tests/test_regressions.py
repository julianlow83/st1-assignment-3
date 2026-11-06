from datetime import datetime
import pytest
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import PatientService, PractitionerService, AppointmentService


def test_f8_01_different_practitioners_same_time_permitted():
    """F8-01 Regression: Verify different practitioners can book at the same datetime (AC-04.2)."""
    store = SmartCareDataStore()
    pat_svc = PatientService(store)
    prac_svc = PractitionerService(store)
    appt_svc = AppointmentService(store)

    pat_svc.register_patient("P101", "Alice Smith")
    pat_svc.register_patient("P102", "Bob Jones")
    prac_svc.register_practitioner("D201", "Dr. Smith", "GP")
    prac_svc.register_practitioner("D202", "Dr. Jones", "Cardiology")

    slot_time = datetime(2026, 11, 1, 10, 0)
    appt1 = appt_svc.book_appointment("A301", "P101", "D201", slot_time)

    # Must succeed for different practitioner D202 without raising ValueError
    appt2 = appt_svc.book_appointment("A302", "P102", "D202", slot_time)
    assert appt2.practitioner.practitioner_id == "D202"
    assert appt2.status == AppointmentStatus.SCHEDULED


def test_f8_02_find_cancelled_appointment_retained():
    """F8-02 Regression: Verify cancelled appointments are retrievable via find_appointment (FR-07 / AC-05.2)."""
    store = SmartCareDataStore()
    pat_svc = PatientService(store)
    prac_svc = PractitionerService(store)
    appt_svc = AppointmentService(store)

    pat_svc.register_patient("P101", "Alice Smith")
    prac_svc.register_practitioner("D201", "Dr. Smith", "GP")

    appt = appt_svc.book_appointment("A301", "P101", "D201", datetime(2026, 11, 1, 10, 0))
    appt_svc.cancel_appointment("A301")

    # Store and service lookups must retrieve the cancelled appointment object
    retained_store = store.find_appointment("A301")
    assert retained_store is not None
    assert retained_store.status == AppointmentStatus.CANCELLED

    retained_svc = appt_svc.find_appointment("A301")
    assert retained_svc.status == AppointmentStatus.CANCELLED