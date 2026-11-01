"""Candidate tests for AC-05.1 (Cancellation State Change) and AC-05.2 (History Retention)."""

from datetime import datetime
import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import AppointmentService, PatientService, PractitionerService


@pytest.fixture
def store_and_services():
    """Fresh in-memory store and service layer for each test."""
    store = SmartCareDataStore()
    patient_svc = PatientService(store)
    practitioner_svc = PractitionerService(store)
    appointment_svc = AppointmentService(store)
    return store, patient_svc, practitioner_svc, appointment_svc


@pytest.fixture
def booked_appointment(store_and_services):
    """Fixture providing a registered patient, practitioner, and a SCHEDULED appointment."""
    store, patient_svc, practitioner_svc, appointment_svc = store_and_services

    patient_svc.register_patient("P101", "Alice Smith")
    practitioner_svc.register_practitioner("D201", "Dr. John Doe", "GP")

    booked = appointment_svc.book_appointment(
        "A301",
        "P101",
        "D201",
        datetime(2026, 11, 1, 10, 0),
    )
    return store, appointment_svc, booked


def test_ac_05_1_cancelled_status_change_happy_path(booked_appointment):
    """AC-05.1: cancelling a scheduled appointment updates status without replacing the object."""
    store, appointment_svc, booked = booked_appointment

    assert booked.status is AppointmentStatus.SCHEDULED

    cancelled = appointment_svc.cancel_appointment("A301")

    assert cancelled is booked
    assert cancelled.status is AppointmentStatus.CANCELLED
    assert appointment_svc.find_appointment("A301") is booked
    assert store.find_appointment("A301") is booked


def test_ac_05_1_repeated_cancellation_rejected(booked_appointment):
    """AC-05.1: a cancelled appointment cannot be cancelled again."""
    _, appointment_svc, booked = booked_appointment

    first_cancellation = appointment_svc.cancel_appointment("A301")

    assert first_cancellation is booked
    assert first_cancellation.status is AppointmentStatus.CANCELLED

    with pytest.raises(ValueError):
        appointment_svc.cancel_appointment("A301")

    retrieved = appointment_svc.find_appointment("A301")
    assert retrieved is booked
    assert retrieved.status is AppointmentStatus.CANCELLED


def test_ac_05_2_session_store_retains_cancelled_appointment_record(booked_appointment):
    """AC-05.2: the cancelled appointment remains stored and retrievable in the session store."""
    store, appointment_svc, booked = booked_appointment

    cancelled = appointment_svc.cancel_appointment("A301")

    assert cancelled is booked
    assert cancelled.status is AppointmentStatus.CANCELLED

    retained = store.find_appointment("A301")
    # Explicit check resolves PyCharm 'Member None of Appointment | None' type inspection
    assert retained is not None
    assert retained is booked
    assert retained.status is AppointmentStatus.CANCELLED

    stored_list = store.list_appointments()
    assert len(stored_list) == 1
    assert stored_list[0] is booked
    assert stored_list[0].status is AppointmentStatus.CANCELLED