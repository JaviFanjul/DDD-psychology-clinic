from assistant.infrastructure.postgres.patient_mapper import PatientMapper


def test_given_a_patient_when_mapping_to_model_then_it_copies_its_id_and_status(patient, patient_model):
    mapped = PatientMapper.to_model(patient=patient)

    assert (mapped.id, mapped.active) == (patient_model.id, patient_model.active)


def test_given_a_model_when_mapping_to_entity_then_it_rebuilds_the_patient(patient_model, patient):
    mapped = PatientMapper.to_entity(model=patient_model)

    assert mapped.id == patient.id
    assert mapped.is_active


def test_given_an_inactive_patient_when_mapping_to_model_and_back_then_it_stays_inactive(
    patient,
):
    patient.deactivate()

    mapped = PatientMapper.to_entity(model=PatientMapper.to_model(patient=patient))

    assert not mapped.is_active
