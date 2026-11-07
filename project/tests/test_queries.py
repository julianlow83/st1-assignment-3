import pytest
from datetime import datetime
from smartcare.domain import Patient, Practitioner, Appointment, AppointmentStatus
from smartcare.queries import appointment_sort_key, select_appointments


def test_select_appointments_practitioner_isolation():
    p = Patient("P1", "Alice")
    doc1 = Practitioner("D1", "Dr. House", "GP")
    doc2 = Practitioner("D2", "Dr. Wilson", "Cardiologist")
    dt = datetime(2026, 10, 1, 9, 0)

    a1 = Appointment("A1", p, doc1, dt)
    a2 = Appointment("A2", p, doc2, dt)

    res = select_appointments([a1, a2], "D1")
    assert res == [a1]
    assert a2 not in res


def test_select_appointments_status_filtering():
    p = Patient("P1", "Alice")
    doc = Practitioner("D1", "Dr. House", "GP")
    dt1 = datetime(2026, 10, 1, 9, 0)
    dt2 = datetime(2026, 10, 1, 10, 0)

    a1 = Appointment("A1", p, doc, dt1)
    a2 = Appointment("A2", p, doc, dt2)
    a2.cancel()  # Status becomes CANCELLED

    # Default (None) includes all
    all_appts = select_appointments([a1, a2], "D1", status=None)
    assert len(all_appts) == 2

    # Scheduled only
    sched_appts = select_appointments([a1, a2], "D1", status=AppointmentStatus.SCHEDULED)
    assert sched_appts == [a1]

    # Cancelled only
    canc_appts = select_appointments([a1, a2], "D1", status=AppointmentStatus.CANCELLED)
    assert canc_appts == [a2]


def test_appointment_sort_key_and_tie_break():
    p = Patient("P1", "Alice")
    doc = Practitioner("D1", "Dr. House", "GP")
    dt = datetime(2026, 10, 1, 9, 0)

    a2 = Appointment("A2", p, doc, dt)
    a1 = Appointment("A1", p, doc, dt)

    res = select_appointments([a2, a1], "D1")
    # Tie-break by appointment_id ascending ("A1" before "A2")
    assert res == [a1, a2]


def test_query_non_mutation_and_identity():
    p = Patient("P1", "Alice")
    doc = Practitioner("D1", "Dr. House", "GP")
    dt = datetime(2026, 10, 1, 9, 0)
    a1 = Appointment("A1", p, doc, dt)

    source = [a1]
    source_copy = list(source)

    res = select_appointments(source, "D1")
    assert res is not source
    assert source == source_copy
    assert res[0] is a1