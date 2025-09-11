from bson import ObjectId

def serialize_document(doc):
    """Converts a MongoDB Document into a JSON - serializable directory."""
    return{
        **doc,
        "id":str(doc["_id"]),
    }