from google.cloud import firestore

# Create a Firestore client
db = firestore.Client(project='crypto-catfish-407213')


def insert_into_firestore(date, index_price, variation, index_target, recommendation):
    # Convert the Timestamp to a string
    date_str = date.date().isoformat()

    doc_ref = db.collection('index_data').document(date_str)
    doc_ref.set({
        'IndexPrice': index_price,
        'Variation': variation,
        'IndexTarget': index_target,
        'Recommendation': recommendation
    })
