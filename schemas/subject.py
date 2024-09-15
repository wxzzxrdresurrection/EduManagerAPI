def single_subject_schema(subject):
    return {
        "id": subject.id,
        "name": subject.name,
        "description": subject.description,
        "created_at": subject.created_at,
        "updated_at": subject.updated_at,
    }