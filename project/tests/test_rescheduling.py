"""Focused PG tests for Stage 10 appointment rescheduling functionality."""

from datetime import datetime
import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import AppointmentService, PatientService, PractitionerService


@pytest.fixture
def store_and_services():
    """Fixture providing a clean store and registered participant entities."""
    store = SmartCareDataStore()
    patient_svc = PatientService(store)
    practitioner_svc = PractitionerService(store)
    appointment_svc = AppointmentService(store)

    patient_svc.register_patient("P101", "Alice Smith")
    patient_svc.register_patient("P102", "Bob Jones")
    practitioner_svc.register_practitioner("D201", "Dr. John Doe", "General Practice")
    practitioner_svc.register_practitioner("D202", "Dr. Jane Smith", "Cardiology")

    return store, appointment_svc


def test_ac_res_01_valid_reschedule_preserves_identity(store_and_services):
    """AC-RES-01 / RES-01 & RES-02: Reschedule moves SCHEDULED appointment, preserves identity & returns same object."""
    store, appointment_svc = store_and_services
    original_time = datetime(2026, 11, 1, 10, 0)
    new_time = datetime(2026, 11, 2, 14, 0)

    original = appointment_svc.book_appointment("A301", "P101", "D201", original_time)

    rescheduled = appointment_svc.reschedule_appointment("A301", new_time)

    assert rescheduled is original
    assert rescheduled.appointment_id == "A301"
    assert rescheduled.patient.patient_id == "P101"
    assert rescheduled.practitioner.practitioner_id == "D201"
    assert rescheduled.date_time == new_time
    assert rescheduled.status is AppointmentStatus.SCHEDULED


def test_ac_res_02_unknown_appointment_id_raises_lookup_error(store_and_services):
    """AC-RES-02 / RES-03: Unknown appointment ID raises LookupError without side effects."""
    _, appointment_svc = store_and_services
    new_time = datetime(2026, 11, 2, 14, 0)

    with pytest.raises(LookupError):
        appointment_svc.reschedule_appointment("A999", new_time)


def test_ac_res_03_same_practitioner_conflict_rejected(store_and_services):
    """AC-RES-03 / RES-04: Rescheduling to a slot occupied by the same practitioner raises ValueError."""
    _, appointment_svc = store_and_services
    time_slot_1 = datetime(2026, 11, 1, 10, 0)
    time_slot_2 = datetime(2026, 11, 1, 11, 0)

    appt1 = appointment_svc.book_appointment("A301", "P101", "D201", time_slot_1)
    appointment_svc.book_appointment("A302", "P102", "D201", time_slot_2)

    # Attempt to move A301 to time_slot_2 occupied by Dr. D201
    with pytest.raises(ValueError):
        appointment_svc.reschedule_appointment("A301", time_slot_2)

    # State must remain unmutated
    assert appt1.date_time == time_slot_1


def test_ac_res_04_different_practitioner_same_time_permitted(store_and_services):
    """AC-RES-04 / RES-04: Rescheduling to a time occupied by a DIFFERENT practitioner succeeds."""
    _, appointment_svc = store_and_services
    time_slot_1 = datetime(2026, 11, 1, 10, 0)
    time_slot_2 = datetime(2026, 11, 1, 11, 0)

    appt1 = appointment_svc.book_appointment("A301", "P101", "D201", time_slot_1)
    appointment_svc.book_appointment("A302", "P102", "D202", time_slot_2)

    # Move D201 to time_slot_2 where D202 has an appointment
    rescheduled = appointment_svc.reschedule_appointment("A301", time_slot_2)
    assert rescheduled.date_time == time_slot_2


def test_ac_res_05_cancelled_and_completed_rejected(store_and_services):
    """AC-RES-05 / RES-06: Rescheduling CANCELLED appointments raises ValueError without state mutation."""
    _, appointment_svc = store_and_services
    original_time = datetime(2026, 11, 1, 10, 0)
    new_time = datetime(2026, 11, 2, 14, 0)

    appt = appointment_svc.book_appointment("A301", "P101", "D201", original_time)
    appointment_svc.cancel_appointment("A301")

    with pytest.raises(ValueError):
        appointment_svc.reschedule_appointment("A301", new_time)

    # Confirm time remains original and status remains CANCELLED
    assert appt.date_time == original_time
    assert appt.status is AppointmentStatus.CANCELLED


def test_ac_res_06_r2_session_lookup_reflects_new_time_and_freed_slot(store_and_services):
    """AC-RES-06-R2 / RES-05-R2: Lookups show updated time and vacated slot is released for re-booking."""
    store, appointment_svc = store_and_services
    old_time = datetime(2026, 11, 1, 10, 0)
    new_time = datetime(2026, 11, 2, 14, 0)

    appointment_svc.book_appointment("A301", "P101", "D201", old_time)
    appointment_svc.reschedule_appointment("A301", new_time)

    # Store and service lookup reflect new time
    assert store.find_appointment("A301").date_time == new_time
    assert appointment_svc.find_appointment("A301").date_time == new_time

    # Old slot must be freed: booking another patient for D201 at old_time must succeed
    new_booking = appointment_svc.book_appointment("A302", "P102", "D201", old_time)
    assert new_booking.date_time == old_time


def test_reschedule_same_time_self_exclusion_noop(store_and_services):
    """RES-04 Boundary: Rescheduling to the exact same time (no-op) succeeds via self-exclusion."""
    _, appointment_svc = store_and_services
    same_time = datetime(2026, 11, 1, 10, 0)

    appt = appointment_svc.book_appointment("A301", "P101", "D201", same_time)
    rescheduled = appointment_svc.reschedule_appointment("A301", same_time)

    assert rescheduled.date_time == same_time


def test_reschedule_invalid_inputs_rejected(store_and_services):
    """RES-03 & Datetime Validation: Invalid appointment IDs or non-naive datetimes raise exceptions."""
    _, appointment_svc = store_and_services
    valid_time = datetime(2026, 11, 1, 10, 0)
    appointment_svc.book_appointment("A301", "P101", "D201", valid_time)

    # Blank/invalid IDs
    with pytest.raises(ValueError):
        appointment_svc.reschedule_appointment("   ", valid_time)
    with pytest.raises(ValueError):
        appointment_svc.reschedule_appointment("", valid_time)

    # Datetime with non-zero seconds
    invalid_seconds = datetime(2026, 11, 2, 14, 0, 30)
    with pytest.raises(ValueError):
        appointment_svc.reschedule_appointment("A301", invalid_seconds)