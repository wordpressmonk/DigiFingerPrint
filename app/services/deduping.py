def firstDeduping(smartpixl_data):
    deduped_data = [{record['RecordID']: record for record in smartpixl_data}]
    return deduped_data

