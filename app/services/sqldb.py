from app import db

# from app.models import FilteredData
'''
This is not used right now, will be used while scaling
'''


def insertFilteredData(company_id, smartpixl_data, email_source='smartpixl', email_status='INVALID'):
    smartpixl_recordId = smartpixl_data.get('RecordID')
    smartpixl_date = smartpixl_data.get('Date')
    email = smartpixl_data.get('EMail', '')
    first_name = smartpixl_data.get('FirstName')
    last_name = smartpixl_data.get('LastName')
    if not email:
        new_entry = FilteredData(companyId=company_id, smartpixl_recordId=smartpixl_recordId,
                                 smartpixl_date=smartpixl_date, first_name=first_name, last_name=last_name)
    else:
        new_entry = FilteredData(companyId=company_id, smartpixl_recordId=smartpixl_recordId, first_name=first_name,
                                 last_name=last_name, smartpixl_date=smartpixl_date, email=email,
                                 email_source=email_source,
                                 email_status=email_status)
    db.session.add(new_entry)
    db.session.commit()
    return new_entry, True
    # except Exception as e:
    #     db.session.rollback()
    #     print("insertFilteredDataERROR: %s" % str(e))
    #     return "insertFilteredDataERROR: %s" % str(e), False

# def bulkInsertFilteredData(company_id, xml_to_pdf_message, email_source='smartpixl', email_status='INVALID'):
#     new_entries = []
#     for record in xml_to_pdf_message:
#         smartpixl_recordId = record.get('RecordID')
#         smartpixl_date = record.get('Date')
#         email = record.get('EMail', '')
#         new_entry = FilteredData(companyId=company_id, smartpixl_recordId=smartpixl_recordId,
#                                  smartpixl_date=smartpixl_date, email=email, email_source=email_source,
#                                  email_status=email_status)
#         new_entries.append(new_entry)
#         print(len(new_entries))
#     db.session.add_all(new_entries)
#     db.session.commit()
#     return "success", True
# except Exception as e:
#     db.session.rollback()
#     print("bulkInsertFilteredDataERROR: %s" % str(e))
#     return "bulkInsertFilteredDataERROR: %s" % str(e), False
